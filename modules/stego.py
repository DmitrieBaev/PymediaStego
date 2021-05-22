import os, sys
# pip install opencv-python
import cv2


class Steganography:
    def __init__(self, degree, i, n, enc_copyright):
        self.D = degree
        self.I = i
        self.N = n
        self.L = len(enc_copyright)
        self.MES = enc_copyright  # Encrypted copyright as message
        self.BMP_HEADER_SIZE = 54
        self.FRAME_ARRAY = []

    def encode_video(self, path_in, path_out, fname):
        capture = cv2.VideoCapture(path_in)
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = capture.get(cv2.CAP_PROP_FPS)
        fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))
        _i = 0
        while True:
            ret, frame = capture.read()
            if not ret:
                break
            _i += 1
            if _i % self.N == 0:
                for _j in range(self.I):
                    ret, frame = capture.read()
                    if not ret:
                        break
                    cv2.imwrite('tmp_1.bmp', frame)
                    self.encode_image(self.D, self.MES, 'tmp_1.bmp')
                    os.remove('tmp_1.bmp')
                    self.FRAME_ARRAY.append(cv2.imread('tmp_2.bmp'))
                    os.remove('tmp_2.bmp')
            else:
                self.FRAME_ARRAY.append(frame)
        capture.release()
        try:
            out = cv2.VideoWriter(f'{path_out}/{fname}', fourcc, fps, size)
            for i in range(len(self.FRAME_ARRAY)):
                out.write(self.FRAME_ARRAY[i])
            out.release()
        finally:
            cv2.destroyAllWindows()

    def encode_image(self, degree, text, image_in_path):
        output_image = open('tmp_2.bmp', 'wb')
        input_image = open(image_in_path, 'rb')
        output_image.write(input_image.read(self.BMP_HEADER_SIZE))
        text_mask, img_mask = self.get_masks(degree)
        for symbol in text:
            for byte_amount in range(0, 8, degree):
                img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
                bits = symbol & text_mask
                bits >>= (8 - degree)
                img_byte |= bits
                output_image.write(img_byte.to_bytes(1, sys.byteorder))
                symbol <<= degree
        output_image.write(input_image.read())
        input_image.close()
        output_image.close()

    def decode_video(self, path_in):
        capture = cv2.VideoCapture(path_in)
        _i = 0
        while True:
            ret, frame = capture.read()
            if not ret:
                break
            _i += 1
            if _i % self.N == 0:
                for _j in range(self.I):
                    ret, frame = capture.read()
                    if not ret:
                        break
                    cv2.imwrite('tmp_1.bmp', frame)
                    if not self.decode_copyright(self.D, self.L, 'tmp_1.bmp'):
                        return False
            else:
                continue
        capture.release()
        return True

    def decode_copyright(self, degree, count_to_read, path_to_bmp):
        text = b''
        encoded_bmp = open(path_to_bmp, 'rb')
        encoded_bmp.seek(self.BMP_HEADER_SIZE)
        _, img_mask = self.get_masks(degree)
        img_mask = ~img_mask
        read = 0
        while read <= count_to_read:
            symbol = 0
            for bits_read in range(0, 8, degree):
                img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
                symbol <<= degree
                symbol |= img_byte
            if chr(symbol) == '\n' and len(os.linesep) == 2:
                read += 1
            read += 1
            text += symbol.to_bytes(1, sys.byteorder)
        encoded_bmp.close()
        os.remove(path_to_bmp)
        return True if text == self.MES else False

    def get_masks(self, degree):
        text_mask = 0b11111111
        img_mask = 0b11111111
        text_mask <<= (8 - degree); text_mask %= 256
        img_mask >>= degree;        img_mask <<= degree
        return text_mask, img_mask

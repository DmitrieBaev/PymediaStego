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
        self.PROPS = f'D={self.D};I={self.I};N={self.N};L={self.L};'.encode()  # Properties for encoding
        self.BMP_HEADER_SIZE = 54
        self.FRAME_ARRAY = []

    def fourcc(self, ext):
        if ext == '.mp4':
            return cv2.VideoWriter_fourcc(*'mp4v')
        elif ext == '.avi':
            return cv2.VideoWriter_fourcc(*'DIVX')
        else:
            raise ValueError

    def encode_video(self, path_in, path_out, fname):
        capture = cv2.VideoCapture(path_in)
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = capture.get(cv2.CAP_PROP_FPS)
        _i = 0
        while True:
            ret, frame = capture.read()
            if not ret:
                break
            _i += 1
            if _i == 1:
                cv2.imwrite('tmp.bmp', frame)
                self.FRAME_ARRAY.append(self.encode_image(self.PROPS, 'tmp.bmp'))
                os.remove('tmp.bmp')
            elif _i % self.N == 0:
                for _j in range(self.I):
                    ret, frame = capture.read()
                    if not ret:
                        break
                    cv2.imwrite('tmp_1.bmp', frame)
                    self.encode_image(self.MES, 'tmp_1.bmp')
                    os.remove('tmp_1.bmp')
                    self.FRAME_ARRAY.append(cv2.imread('tmp_2.bmp'))
                    os.remove('tmp_2.bmp')
            else:
                self.FRAME_ARRAY.append(frame)
        capture.release()

        fname_rpart = fname[fname.rfind('.'):]
        fname_lpart = fname[:fname.rfind('.')]
        os.mkdir(f'{path_out}/{fname_lpart}')
        out = cv2.VideoWriter(f'{path_out}/{fname_lpart}/{fname}', self.fourcc(fname_rpart), fps, size)
        for i in range(len(self.FRAME_ARRAY)):
            out.write(self.FRAME_ARRAY[i])
        out.release()
        cv2.destroyAllWindows()
        return f'{path_out}/{fname_lpart}'
        # compile audio

    def encode_image(self, text, image_in_path):
        output_image = open('tmp_2.bmp', 'wb')
        input_image = open(image_in_path, 'rb')
        output_image.write(input_image.read(self.BMP_HEADER_SIZE))
        text_mask, img_mask = self.get_masks()
        for symbol in text:
            for byte_amount in range(0, 8, self.D):
                img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
                bits = symbol & text_mask
                bits >>= (8 - self.D)
                img_byte |= bits
                output_image.write(img_byte.to_bytes(1, sys.byteorder))
                symbol <<= self.D
        output_image.write(input_image.read())
        input_image.close()
        output_image.close()

    def decode_video(self):
        pass

    def decode_image(self):
        pass

    def get_masks(self):
        text_mask = 0b11111111
        img_mask = 0b11111111
        text_mask <<= (8 - self.D); text_mask %= 256
        img_mask >>= self.D;        img_mask <<= self.D
        return text_mask, img_mask

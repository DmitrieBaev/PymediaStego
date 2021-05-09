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
        # print(f'{ext} => {ext == ".mp4"}')
        # if ext == '.3gp' or ext == '.mov' or ext == '.mp4':
        #     return cv2.VideoWriter_fourcc(*'MJPG')
        # elif ext == '.mkv':
        #     return cv2.VideoWriter_fourcc(*'H264')
        # elif ext == '.avi' or ext == '.flv':
        #     return cv2.VideoWriter_fourcc(*'DIVX')
        # else:
        #     raise ValueError
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




#
# def encode_image(input_img_name, output_img_name, txt_file, degree):
#     """
#     This function reads text from the txt_file file and encodes it
#     by bits from input_img to output_img.
#     Because every byte of image can contain maximum 8 bits of information,
#     text size should be less than (image_size * degree / 8 - BMP_HEADER_SIZE)
#     :param input_img_name: name of 24-bit BMP original image
#     :param output_img_name: name of 24-bit BMP encoded image (will create or overwrite)
#     :param txt_file: name of file containing text to be encoded in output_img
#     :param degree: number of bits from byte (1/2/4/8) that are taken to encode text data in image.
#     :return: True if function succeeds else False
#     """
#
#     if degree not in [1, 2, 4, 8]:
#         print("Degree value can be only 1/2/4/8")
#         return False
#
#     text_len = os.stat(txt_file).st_size
#     img_len = os.stat(input_img_name).st_size
#
#     if text_len >= img_len * degree / 8 - BMP_HEADER_SIZE:
#         print("Too long text")
#         return False
#
#     text = open(txt_file, 'r')
#     input_image = open(input_img_name, 'rb')
#     output_image = open(output_img_name, 'wb')
#
#     bmp_header = input_image.read(BMP_HEADER_SIZE)
#     output_image.write(bmp_header)
#
#     text_mask, img_mask = create_masks(degree)
#
#     while True:
#         symbol = text.read(1)
#         if not symbol:
#             break
#         symbol = ord(symbol)
#
#         for byte_amount in range(0, 8, degree):
#             img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
#             bits = symbol & text_mask
#             bits >>= (8 - degree)
#             img_byte |= bits
#
#             output_image.write(img_byte.to_bytes(1, sys.byteorder))
#             symbol <<= degree
#
#     output_image.write(input_image.read())
#
#     text.close()
#     input_image.close()
#     output_image.close()
#
#     return True
#
#
# def decode_image(encoded_img, output_txt, symbols_to_read, degree):
#     """
#     This function takes symbols_to_read bytes from encoded image and retrieves hidden
#     information from them with a given degree.
#     Because every byte of image can contain maximum 8 bits of information,
#     text size should be less than (image_size * degree / 8 - BMP_HEADER_SIZE)
#     :param encoded_img: name of 24-bit BMP encoded image
#     :param output_txt: name of txt file where result should be written
#     :param symbols_to_read: amount of encoded symbols in image
#     :param degree: number of bits from byte (1/2/4/8) that are taken to encode text data in image
#     :return: True if function succeeds else False
#     """
#     if degree not in [1, 2, 4, 8]:
#         print("Degree value can be only 1/2/4/8")
#         return False
#
#     img_len = os.stat(encoded_img).st_size
#
#     if symbols_to_read >= img_len * degree / 8 - BMP_HEADER_SIZE:
#         print("Too much symbols to read")
#         return False
#
#     text = open(output_txt, 'w', encoding='utf-8')
#     encoded_bmp = open(encoded_img, 'rb')
#
#     encoded_bmp.seek(BMP_HEADER_SIZE)
#
#     _, img_mask = create_masks(degree)
#     img_mask = ~img_mask
#
#     read = 0
#     while read < symbols_to_read:
#         symbol = 0
#
#         for bits_read in range(0, 8, degree):
#             img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
#             symbol <<= degree
#             symbol |= img_byte
#
#         if chr(symbol) == '\n' and len(os.linesep) == 2:
#             read += 1
#
#         read += 1
#         text.write(chr(symbol))
#
#     text.close()
#     encoded_bmp.close()
#     return True
#
#
# def create_masks(degree):
#     """
#     Create masks for taking bits from text bytes and
#     putting them to image bytes.
#     :param degree: number of bits from byte that are taken to encode text data in image
#     :return: a mask for a text and a mask for an image
#     """
#     text_mask = 0b11111111
#     img_mask = 0b11111111
#
#     text_mask <<= (8 - degree)
#     text_mask %= 256
#     img_mask >>= degree
#     img_mask <<= degree
#
#     return text_mask, img_mask
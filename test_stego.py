import sys, os, unittest


class Steganography:
    def __init__(self, d=4):
        self.DEGREE = d

    def encode_image(self, _CR):
        output_image = open('data/tmp/frame_stego.bmp', 'wb')
        input_image = open('data/tmp/frame_10.bmp', 'rb')
        output_image.write(input_image.read(54))
        text_mask, img_mask = self.get_masks(self.DEGREE)
        for symbol in _CR:
            for byte_amount in range(0, 8, self.DEGREE):
                img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
                bits = symbol & text_mask
                bits >>= (8 - self.DEGREE)
                img_byte |= bits
                output_image.write(img_byte.to_bytes(1, sys.byteorder))
                symbol <<= self.DEGREE
        output_image.write(input_image.read())
        input_image.close()
        output_image.close()

    def decode_image(self, _CR):
        text = b''
        encoded_bmp = open('data/tmp/frame_stego.bmp', 'rb')
        encoded_bmp.seek(54)
        _, img_mask = self.get_masks(self.DEGREE)
        img_mask = ~img_mask
        read = 0
        while read <= len(_CR):
            symbol = 0
            for bits_read in range(0, 8, self.DEGREE):
                img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
                symbol <<= self.DEGREE
                symbol |= img_byte
            if chr(symbol) == '\n' and len(os.linesep) == 2:
                read += 1
            read += 1
            text += symbol.to_bytes(1, sys.byteorder)
        encoded_bmp.close()
        return True if text == _CR else False

    def get_masks(self, degree=8):
        text_mask = 0b11111111
        img_mask = 0b11111111
        text_mask <<= (8 - degree)
        text_mask %= 256
        img_mask >>= degree
        img_mask <<= degree
        return text_mask, img_mask


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.Stego = Steganography()
        self.CR = 'Copyright by okeyw.\nAll Rights Reserved.'.encode()

    def test_steganography(self):
        self.Stego.encode_image(self.CR)
        self.assertEqual(self.Stego.decode_image(self.CR), True)


if __name__ == '__main__':
    unittest.main()
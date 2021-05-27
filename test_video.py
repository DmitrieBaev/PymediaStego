import unittest
from modules.stego import Steganography


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.Stego = Steganography(degree=4, i=2, n=10, enc_copyright='Copyright by okeyw.\nAll Rights Reserved.'.encode())

    def test_steganography(self):
        self.Stego.encode_video(r'data\vid\good_job.divx.avi',
                                r'data',
                                'good_job.divx.avi')
        self.assertEqual(self.Stego.decode_video(r'data\tmp\good_job.divx.avi'), True)


if __name__ == '__main__':
    unittest.main()
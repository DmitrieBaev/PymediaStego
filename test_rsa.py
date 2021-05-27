import unittest
from modules.rsa import Encryptor as ASyncEncr

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.RSA = ASyncEncr()
        self.path_to_videofile = r'data\vid\good_job.divx.avi'
        self.hash = b'm=Z\xe0j\x8cO@E!O\xc6Z9\xbb\xf6\x9001\xbaC\x82\xd0\xcd\xf0HY' \
                    b'\xab\x8f\xae\xfd\x03\xacd7w\xad(*\\\x8a\xc2\xb8@U_\xbc\x82\xa6' \
                    b'\xce\x8b\xca\x08P\x95*N\xa9\xa7\x9a\xe3\x08\xec\xfb\x03C\xe6\x9b' \
                    b'\x98\xa6\\$U#\xcdm\x18\xeb ;\xed\xbe\x97-`\x02\xd8\x90\xc78\x02' \
                    b'\xa3}\xf2\xe8n\xbb\x0e\xda\xe9\xfd\xeb\x94\x08\x95\xc7"\x15\x04' \
                    b'\xc6d\xacw\xd4\xce\xffG\xe5\xc4{\xa8\xe6ytV\xfcX$'

    def test_file_hashing(self):
        self.assertEqual(self.RSA.get_eds(self.path_to_videofile), self.hash)

    def test_hash_verifying(self):
        self.assertEqual(self.RSA.verify_eds(self.path_to_videofile, self.hash), True)


if __name__ == '__main__':
    unittest.main()
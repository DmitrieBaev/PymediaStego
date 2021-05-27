import unittest
from modules.aes import Encryptor as SyncEncr

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.AES = SyncEncr()

    def test_sync_crypt(self):
        CR = 'Copyright by okeyw.\nAll Rights Reserved.'.encode()
        _CR = self.AES.encrypt(CR)
        CR_ = self.AES.decrypt(_CR)
        self.assertEqual(CR_ == CR, True)


if __name__ == '__main__':
    unittest.main()
# pip install pycryptodome
from Crypto import Random
from Crypto.Cipher import AES


class Encryptor:
    def __init__(self,
                 default_key='2yDynDCk5Njsvq2m'.encode(),
                 option='use_default',
                 key_data=''):
        if option == 'use_default':
            self.key = default_key
        elif option == 'generate':
            self.key = key_data.encode("utf-8")[:16] if not key_data == '' else '2yDynDCk5Njsvq2m'.encode()
        else:
            self.key=b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, msg_byte):
        msg_byte = self.pad(msg_byte)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return iv + cipher.encrypt(msg_byte)

    def decrypt(self, cipher_byte):
        iv = cipher_byte[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        plaintext = cipher.decrypt(cipher_byte[AES.block_size:])
        return plaintext.rstrip(b"\0")

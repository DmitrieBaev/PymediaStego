from modules.aes import Encryptor as SyncEncr
from modules.rsa import Encryptor as ASyncEncr

COPYRIGHT = 'Copyright: © help.py,\n06.04.2021 12:47, okeyw\nAll Rights Reserved.'


if __name__ == '__main__':
    key = '2yDynDCk5Njsvq2m'.encode()
    copyright_byte = COPYRIGHT.encode()

    AES = SyncEncr(key)
    copyright_encrypted = AES.encrypt(copyright_byte)
    copyright_decrypted = AES.decrypt(copyright_encrypted)

    RSA = ASyncEncr()
    signature = RSA.encrypt('06.04.2021 12:47'.encode())
    correct = RSA.decrypt('06.04.2021 12:47'.encode(), signature)
    print(f'ЭЦП корректна? {correct}')

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import os


class Encryptor:
    def __init__(self):
        self.PR = ''
        self.PU = ''
        self.check_keys()

    def check_keys(self):
        if not os.path.exists('resources/var/PR.pem') or \
           not os.path.exists('resources/var/PU.pem'):
            print('Ключей не существует')
            self.create_keys()
        else:
            print('Ключи существуют')
            self.load_keys()

    def create_keys(self):
        print('Создание новых пар ключей')
        self.PR = RSA.generate(1024)
        self.PU = self.PR.public_key()
        open('resources/var/PR.pem', 'wb').write(bytes(self.PR.exportKey('PEM')))
        open('resources/var/PU.pem', 'wb').write(bytes(self.PU.exportKey('PEM')))
        print('Создание новых пар ключей успешно произведено')

    def load_keys(self):
        print("Запускается процесс импорта ключей")
        self.PR = RSA.importKey(open('resources/var/PR.pem').read())
        self.PU = RSA.importKey(open('resources/var/PU.pem').read())
        print("Успешный импорт ключей")

    def encrypt(self, creation_file_date):
        h = SHA256.new(creation_file_date)
        print(h.digest())
        return PKCS1_v1_5.new(self.PR).sign(h)

    def decrypt(self, creation_file_date, signature):
        h = SHA256.new(creation_file_date)
        print(h.digest())
        if PKCS1_v1_5.new(self.PU).verify(h, signature):
            return True
        else:
            return False
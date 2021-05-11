# pip install pycryptodome
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
            self.create_keys()
        else:
            self.load_keys()

    def create_keys(self):
        self.PR = RSA.generate(1024)
        self.PU = self.PR.public_key()
        open('resources/var/PR.pem', 'wb').write(bytes(self.PR.exportKey('PEM')))
        open('resources/var/PU.pem', 'wb').write(bytes(self.PU.exportKey('PEM')))

    def load_keys(self):
        self.PR = RSA.importKey(open('resources/var/PR.pem').read())
        self.PU = RSA.importKey(open('resources/var/PU.pem').read())

    @staticmethod
    def get_hash(path_to_file):
        _hash, _buf = SHA256.new(), 65536
        with open(path_to_file, 'rb') as f:
            while True:
                data = f.read(_buf)
                if not data:
                    break
                _hash.update(data)
        return _hash

    def get_eds(self, path_to_file):
        h = self.get_hash(path_to_file)
        return PKCS1_v1_5.new(self.PR).sign(h)

    def verify_eds(self, path_to_file, signature):
        h = self.get_hash(path_to_file)
        if PKCS1_v1_5.new(self.PU).verify(h, signature):
            return True
        else:
            return False
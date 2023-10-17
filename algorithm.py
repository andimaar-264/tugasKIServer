from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import os.path
from os import listdir
from os.path import isfile, join

class AESEncryptor:
    def __init__(self, key: str):
        if len(key) == 16:
            self.key_length = 16
        elif len(key) == 24:
            self.key_length = 24
        elif len(key) == 32:
            self.key_length = 32
        else:
            raise Exception("Key Length invalid.")
        self.key = key.encode('ASCII')
        self.iv = Random.new().read(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        
    def encrypt(self, message: str):
        plaintext = message
        ciphertext = self.cipher.encrypt(pad(plaintext, AES.block_size))
        print(plaintext)
        print(ciphertext)
        print(self.cipher.iv)
        return self.iv + ciphertext
    
    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plainttext = fo.read()
        enc = self.encrypt(plainttext)
        with open (file_name+'.enc', 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, cipherText):
        plainText = self.cipher.decrypt(cipherText)
        return plainText
    
    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            iv = fo.read(self.key_length)
            self.iv = iv
            self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext)
        plaintext = unpad(dec, AES.block_size)
        print(plaintext)
        with open(file_name[:4], 'wb') as fo:
            fo.write(plaintext)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subDirList, fileList in os.walk(dir_path + '/files'):
            for fname in fileList:
                dirs.append(dirName+"\\"+fname)
        return dirs
    
    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)
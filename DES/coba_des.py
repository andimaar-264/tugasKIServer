# from flask import Flask, request, jsonify
# from Crypto.Cipher import DES
# from Crypto.Random import get_random_bytes
# import base64

# app = Flask(__name__)

# # Set a secret key for session management
# app.secret_key = "your_secret_key"

# # Replace with a secure key for encryption
# key = get_random_bytes(8)

# @app.route('/encrypt', methods=['POST'])
# def encrypt_data():
#     data = request.form.get('data')
#     data_bytes = data.encode('utf-8')
    
#     # Create a DES cipher object
#     des = DES.new(key, DES.MODE_ECB)
    
#     # Calculate the number of bytes needed for padding
#     padding_length = 8 - (len(data_bytes) % 8)
    
#     # Pad the data with null bytes
#     padded_data = data_bytes + b'\0' * padding_length
    
#     # Encrypt the padded data
#     encrypted_data = des.encrypt(padded_data)
    
#     # Encode the encrypted data as base64
#     encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    
#     return jsonify({"encrypted_data": encrypted_data_base64})

# @app.route('/decrypt', methods=['POST'])
# def decrypt_data():
#     encrypted_data_base64 = request.form.get('encrypted_data')
    
#     try:
#         # Ensure that the string length is a multiple of 4 by adding padding characters
#         while len(encrypted_data_base64) % 4 != 0:
#             encrypted_data_base64 += '='

#         encrypted_data = base64.b64decode(encrypted_data_base64)
    
#         # Create a DES cipher object
#         des = DES.new(key, DES.MODE_ECB)
    
#         # Decrypt the data
#         decrypted_data = des.decrypt(encrypted_data)
    
#         # Split the decrypted data at the first null byte and return the non-null part as a string
#         data = decrypted_data.split(b'\0', 1)[0].decode('utf-8')
    
#         return jsonify({"decrypted_data": data})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)

#================================================================CBC================================================

# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.padding import PKCS7
# from cryptography.hazmat.primitives import serialization
# import os

# # Secret key for TripleDES encryption (24 bytes)
# secret_key = os.urandom(24)  # Replace with your own key

# # Data to be encrypted
# data = b'This is some secret data.'

# # Generate a random IV (Initialization Vector) (8 bytes for TripleDES)
# iv = os.urandom(8)

# # Create a TripleDES cipher in CBC mode
# cipher = Cipher(algorithms.TripleDES(secret_key), modes.CBC(iv), backend=default_backend())

# # Encrypt the data
# encryptor = cipher.encryptor()
# padder = PKCS7(64).padder()  # 64 is the block size for TripleDES
# padded_data = padder.update(data) + padder.finalize()
# cipher_text = encryptor.update(padded_data) + encryptor.finalize()

# # Decrypt the data
# decryptor = cipher.decryptor()
# plain_text = decryptor.update(cipher_text) + decryptor.finalize()

# # Remove the padding
# unpadder = PKCS7(64).unpadder()
# original_data = unpadder.update(plain_text) + unpadder.finalize()

# # Print the results
# print(f'Encrypted data (TripleDES CBC): {cipher_text.hex()}')
# print(f'Decrypted data (TripleDES CBC): {original_data.decode()}')


#================================================================CFB============================================================
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# import os

# # Secret key for DES encryption
# secret_key = os.urandom(24)  # Replace with your own key

# # Data to be encrypted
# data = b'This is some secret data.'

# # Generate a random IV (Initialization Vector)
# iv = os.urandom(8)

# # Create a DES cipher in CFB mode
# cipher = Cipher(algorithms.TripleDES(secret_key), modes.CFB(iv), backend=default_backend())

# # Encrypt the data
# encryptor = cipher.encryptor()
# cipher_text = encryptor.update(data) + encryptor.finalize()

# # Decrypt the data
# decryptor = cipher.decryptor()
# plaintext = decryptor.update(cipher_text) + decryptor.finalize()

# # Print the results
# print(f'Encrypted data (TripleDES CFB): {cipher_text.hex()}')
# print(f'Decrypted data (TripleDES CFB): {plaintext.decode()}')


#================================================================OFB================================================================
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# import os

# # Secret key for DES encryption
# secret_key = b'Sixteen byte key'  # Replace with your own key

# # Data to be encrypted
# data = b'This is some secret data.'

# # Generate a random IV (Initialization Vector)
# iv = os.urandom(8)

# # Create a DES cipher in OFB mode
# cipher = Cipher(algorithms.TripleDES(secret_key), modes.OFB(iv), backend=default_backend())

# # Encrypt the data
# encryptor = cipher.encryptor()
# cipher_text = encryptor.update(data) + encryptor.finalize()

# # Decrypt the data
# decryptor = cipher.decryptor()
# plaintext = decryptor.update(cipher_text) + decryptor.finalize()

# # Print the results
# print(f'Encrypted data (TripleDES OFB): {cipher_text.hex()}')
# print(f'Decrypted data (TripleDES OFB): {plaintext.decode()}')


#================================================================CTR================================
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import os

# Secret key for DES encryption (must be 8 bytes)
secret_key = os.urandom(8)

# Data to be encrypted
data = b'This is some secret data.'

# Generate a random nonce
nonce = get_random_bytes(4)

# Create a DES cipher in CTR mode
cipher = DES.new(secret_key, DES.MODE_CTR, nonce=nonce)

# Encrypt the data
cipher_text = cipher.encrypt(data)

# Decrypt the data
cipher = DES.new(secret_key, DES.MODE_CTR, nonce=nonce)  # Recreate the cipher with the same nonce for decryption
plaintext = cipher.decrypt(cipher_text)

# Print the results
print(f'Encrypted data (DES CTR): {cipher_text.hex()}')
print(f'Decrypted data (DES CTR): {plaintext.decode()}')



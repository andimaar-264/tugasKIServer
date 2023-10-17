from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import base64
import os

app = Flask(__name__)

# Generate a random TripleDES key (24 bytes)
secret_key = os.urandom(24)

@app.route('/encrypt', methods=['POST'])
def encrypt_data_cbc():
    data = request.form.get('data').encode('utf-8')
    
    # Generate a random IV (Initialization Vector) (8 bytes for TripleDES)
    iv = os.urandom(8)
    
    # Create a TripleDES cipher in CBC mode
    cipher = Cipher(algorithms.TripleDES(secret_key), modes.CBC(iv), backend=default_backend())
    
    # Encrypt the data
    encryptor = cipher.encryptor()
    padder = PKCS7(64).padder()  # 64 is the block size for TripleDES
    padded_data = padder.update(data) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine IV and encrypted data and encode as base64
    iv_and_data = iv + cipher_text
    encrypted_data_base64 = base64.b64encode(iv_and_data).decode('utf-8')
    
    return jsonify({"encrypted_data": encrypted_data_base64})

@app.route('/decrypt', methods=['POST'])
def decrypt_data_cbc():
    encrypted_data_base64 = request.form.get('encrypted_data')
    
    try:
        # Ensure that the string length is a multiple of 4 by adding padding characters
        while len(encrypted_data_base64) % 4 != 0:
            encrypted_data_base64 += '='

        # Decode base64
        iv_and_data = base64.b64decode(encrypted_data_base64.encode('utf-8'))

        # Extract IV and encrypted data
        iv = iv_and_data[:8]
        encrypted_data = iv_and_data[8:]
    
        # Create a TripleDES cipher in CBC mode
        cipher = Cipher(algorithms.TripleDES(secret_key), modes.CBC(iv), backend=default_backend())

        # Decrypt the data
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove the padding
        unpadder = PKCS7(64).unpadder()  # Use the same block size (64) as during encryption
        original_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
        return jsonify({"Decrypted data (TripleDES CBC)": original_data.decode()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

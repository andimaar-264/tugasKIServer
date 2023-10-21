from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)

# Secret key for DES encryption
secret_key = os.urandom(24)   # Replace with your own key

# Generate a random IV (Initialization Vector)
iv = os.urandom(8)

@app.route('/encrypt', methods=['POST'])
def encrypt_des_ofb():
    data = request.form.get('data').encode('utf-8')

    # Create a TripleDES cipher in OFB mode
    cipher = Cipher(algorithms.TripleDES(secret_key), modes.OFB(iv), backend=default_backend())

    # Encrypt the data
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()

    return jsonify({"encrypted_data": cipher_text.hex()})

@app.route('/decrypt', methods=['POST'])
def decrypt_des_ofb():
    encrypted_data_hex = request.form.get('encrypted_data')

    try:
        encrypted_data = bytes.fromhex(encrypted_data_hex)

        # Create a TripleDES cipher in OFB mode with the same IV
        cipher = Cipher(algorithms.TripleDES(secret_key), modes.OFB(iv), backend=default_backend())

        # Decrypt the data
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

        return jsonify({"decrypted_data": plaintext.decode()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

app = Flask(__name__)

# Generate a random TripleDES key (24 bytes)
secret_key = os.urandom(24)

# Generate a random IV (Initialization Vector)
iv = os.urandom(8)

@app.route('/encrypt', methods=['POST'])
def encrypt_des_cfb():
    data = request.form.get('data').encode('utf-8')

    # Create a TripleDES cipher in CFB mode
    cipher = Cipher(algorithms.TripleDES(secret_key), modes.CFB(iv), backend=default_backend())

    # Encrypt the data
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()

    # Encode the encrypted data as base64
    encrypted_data_base64 = base64.b64encode(cipher_text).decode('utf-8')

    return jsonify({"encrypted_data": encrypted_data_base64})

@app.route('/decrypt', methods=['POST'])
def decrypt_des_cfb():
    encrypted_data_base64 = request.form.get('encrypted_data')

    try:
        # Decode base64 to get the binary encrypted data
        encrypted_data = base64.b64decode(encrypted_data_base64)

        # Create a TripleDES cipher in CFB mode with the same IV
        cipher = Cipher(algorithms.TripleDES(secret_key), modes.CFB(iv), backend=default_backend())

        # Decrypt the data
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

        # Decode the decrypted binary data as UTF-8 text
        decrypted_text = plaintext.decode('utf-8')

        return jsonify({"decrypted_data": decrypted_text})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)





# @app.route('/decrypt', methods=['POST'])
# def decrypt_des_cfb():
#     encrypted_data_hex = request.form.get('encrypted_data')

#     try:
#         encrypted_data = bytes.fromhex(encrypted_data_hex)

#         # Create a TripleDES cipher in CFB mode
#         iv = os.urandom(8)
#         cipher = Cipher(algorithms.TripleDES(secret_key), modes.CFB(iv), backend=default_backend())

#         # Decrypt the data
#         decryptor = cipher.decryptor()
#         plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

#         return jsonify({"decrypted_data": plaintext.hex()})
#     except Exception as e:
#         return jsonify({"error": str(e)})

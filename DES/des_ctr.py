from flask import Flask, request, jsonify
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

app = Flask(__name__)

# Generate a random secret key for DES encryption (must be 8 bytes)
secret_key = get_random_bytes(8)

# Initialize the nonce as a global variable
nonce = None

@app.route('/encrypt', methods=['POST'])
def encrypt_des_ctr():
    data = request.form['data'].encode('utf-8')

    # Generate a random nonce (must be 4 bytes)
    global nonce
    nonce = get_random_bytes(4)

    # Create a DES cipher in CTR mode
    cipher = DES.new(secret_key, DES.MODE_CTR, nonce=nonce)

    # Encrypt the data
    cipher_text = cipher.encrypt(data)

    return jsonify({'encrypted_data': cipher_text.hex()})

@app.route('/decrypt', methods=['POST'])
def decrypt_des_ctr():
    try:
        if nonce is None:
            return "Nonce not available", 400

        encrypted_data = bytes.fromhex(request.form['encrypted_data'])

        # Recreate the cipher with the same nonce for decryption
        cipher = DES.new(secret_key, DES.MODE_CTR, nonce=nonce)

        # Decrypt the data
        plaintext = cipher.decrypt(encrypted_data)

        return jsonify({'decrypted_data': plaintext.decode('utf-8')})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

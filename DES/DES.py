from flask import Flask, request, jsonify, send_from_directory, Response
import psycopg2
import os
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

app = Flask(__name__)

# Configure database connection
database = psycopg2.connect(

)


# Configure encryption parameters
SECRET_KEY = os.urandom(24)  # Store this securely
ENCRYPTION_KEY = os.urandom(24)  # Use a secure key for encryption

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Create a new user in userss
        cursor = database.cursor()
        cursor.execute("INSERT INTO userss (username, email, password) VALUES (%s, %s, %s) RETURNING user_id", (username, email, password))
        new_user_id = cursor.fetchone()[0]
        database.commit()
        cursor.close()

        return jsonify({"message": "User created successfully with user_id: " + str(new_user_id)})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.form.get('user_id')
    file = request.files['file']

    if file:
        try:
            # Store the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_file.txt')
            file.save(file_path)

            iv = os.urandom(8) 

            # Create a Cipher object for DES in CBC mode with the IV
            cipher = Cipher(algorithms.TripleDES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            file_data = open(file_path, 'rb').read()

            # Apply PKCS7 padding to the file data
            padder = PKCS7(64).padder()
            padded_file_data = padder.update(file_data) + padder.finalize()

            # Encrypt the padded file data
            encrypted_file_data = encryptor.update(padded_file_data) + encryptor.finalize()

            # Store the encrypted data in a text file
            encrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_encrypted_file.txt')
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_file_data)

            cursor = database.cursor()
            cursor.execute("UPDATE userss SET file_name = %s, file_data = %s, iv = %s WHERE user_id = %s",
                           ('file', encrypted_file_data, iv, user_id))
            database.commit()
            cursor.close()

            return jsonify({"message": "File uploaded and encrypted successfully."})
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "No File file provided."})


@app.route('/get_decrypted/<user_id>', methods=['GET'])
def get_decrypted(user_id):
    try:
        # Retrieve the encrypted file data and IV from the database based on user_id
        cursor = database.cursor()
        cursor.execute("SELECT file_data, iv FROM userss WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            encrypted_file_data, iv = result
            # Decrypt the file using DES in CBC mode
            cipher = Cipher(algorithms.TripleDES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_file_data = decryptor.update(encrypted_file_data) + decryptor.finalize()

            # Unpad the decrypted data using PKCS7
            unpadder = PKCS7(64).unpadder()
            unpadded_data = unpadder.update(decrypted_file_data) + unpadder.finalize()

            # Create a response with the decrypted data
            response = Response(unpadded_data)
            return response

        return jsonify({"error": "File not found for the given user."})

    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import psycopg2
import base64
import os

app = Flask(__name__)

# Replace with your database configuration
# You should use a real database like PostgreSQL or MySQL for this purpose
database = psycopg2.connect(
    dbname="KIJ",
    user="postgres",
    password="5025201075",
    port="5432"  # Default PostgreSQL port
)

# Generate a random TripleDES key (24 bytes)
secret_key = os.urandom(24)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/store_private_data', methods=['POST'])
def store_private_data():
    user_id = request.form.get('user_id')
    private_data = request.form.get('private_data')
    # Store private data in the database using the user_id as the key
    database[user_id] = private_data
    return jsonify({"message": "Private data stored successfully."})

@app.route('/upload_id_card', methods=['POST'])
def upload_id_card():
    user_id = request.form.get('user_id')
    id_card = request.files['id_card']
    if id_card:
        # Save the ID card file to the uploads directory
        id_card.save(os.path.join(app.config['UPLOAD_FOLDER'], user_id + '_id_card.jpg'))
        return jsonify({"message": "ID card uploaded successfully."})
    return jsonify({"error": "No ID card file provided."})

@app.route('/upload_document', methods=['POST'])
def upload_document():
    user_id = request.form.get('user_id')
    document = request.files['document']
    if document:
        # Save the document file to the uploads directory
        document.save(os.path.join(app.config['UPLOAD_FOLDER'], user_id + '_document.pdf'))
        return jsonify({"message": "Document uploaded successfully."})
    return jsonify({"error": "No document file provided."})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    user_id = request.form.get('user_id')
    video = request.files['video']
    if video:
        # Save the video file to the uploads directory
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], user_id + '_video.mp4'))
        return jsonify({"message": "Video uploaded successfully."})
    return jsonify({"error": "No video file provided."})

@app.route('/get_file/<user_id>/<file_type>', methods=['GET'])
def get_file(user_id, file_type):
    # Define a route to access uploaded files
    return send_from_directory(app.config['UPLOAD_FOLDER'], f'{user_id}_{file_type}')

@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    try:
        # Create a cursor to interact with the database
        cursor = database.cursor()

        # Execute a SELECT query to fetch all records from the "users" table
        cursor.execute("SELECT * FROM users")

        # Fetch all the rows from the result set
        rows = cursor.fetchall()

        # Define a list to store the user data
        user_data = []

        # Iterate through the rows and convert them to a list of dictionaries
        for row in rows:
            user_id, username, email, password, registration_date = row
            user_data.append({
                "user_id": user_id,
                "username": username,
                "email": email,
                "password": password,
                "registration_date": registration_date.isoformat()  # Convert to ISO format for JSON
            })

        # Close the cursor
        cursor.close()

        # Return the user data as JSON
        return jsonify({"users": user_data})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

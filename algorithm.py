from Crypto.Cipher import ARC4
import hashlib
import time
import getpass
import datetime

# Storing the username and password
users = [
    {"username": "user1", "password_hash": hashlib.sha256("123".encode()).hexdigest()},
    {"username": "user2", "password_hash": hashlib.sha256("123".encode()).hexdigest()}
]

# verifying user
def verify_user(username, password):
    for user in users:
        if user["username"] == username and user["password_hash"] == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False

# User inputs username and password
input_username = input("Enter your username: ")
#input_password = input("Enter your password: ")
input_password = getpass.getpass("Enter your password: ")

if verify_user(input_username, input_password):
    print("Authentication successful")
    
    # function to encrypt
    def encrypt_file(input_file, output_file, key):
        rc4 = ARC4.new(key)
        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(1024)
                if not chunk:
                    break
                encrypted_chunk = rc4.encrypt(chunk)
                outfile.write(encrypted_chunk)

    # function to decrypt
    def decrypt_file(input_file, output_file, key):
        rc4 = ARC4.new(key)
        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(1024)
                if not chunk:
                    break
                decrypted_chunk = rc4.decrypt(chunk)
                outfile.write(decrypted_chunk)
                
    # Key. Letter b -> byte. The string will be treated as byte object. Removing it will result in error
    key = b'secret'
    
    while True:
        command = input("encrypt (e), decrypt (d), or exit (x)? ")
        
        if command == 'e':
            input_file = input("Enter your file: ")
            # Separate the file name and extension
            base_name, file_extension = input_file.rsplit('.', 1)
            # Generate a timestamp
            timestamp = datetime.datetime.now().strftime("%H%M%S-%d%m%y")
            # Append "encrypted" to the file name
            output_file = f"{base_name}-e-{timestamp}.{file_extension}"
            
            # Encrypt the file
            start_time = time.time()
            encrypt_file(input_file, output_file, key) 
            end_time = time.time()
            running_time = end_time - start_time
            print('Running time: ', running_time)
            
        elif command == 'd':
            input_file = input("Enter your file: ")
            # Separate the file name and extension
            base_name, file_extension = input_file.rsplit('.', 1)
            # Generate a timestamp
            timestamp = datetime.datetime.now().strftime("%H%M%S-%d%m%y")
            # Append "encrypted" to the file name
            output_file = f"{base_name}-d-{timestamp}.{file_extension}"

            # Decrypt the file
            start_time = time.time()
            decrypt_file(input_file, output_file, key)
            end_time = time.time()
            running_time = end_time - start_time
            print('Running time: ', running_time)
                  
        elif command == 'x':
            break 
        
        else:
            print("Invalid command. Please input e, d, or x.")
        
else:
    print("Authentication failed")

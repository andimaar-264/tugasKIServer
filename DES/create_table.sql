CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    registration_date TIMESTAMP
);

CREATE TABLE documents (
    document_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    document_name VARCHAR(255) NOT NULL,
    document_data BYTEA, -- For storing binary data
    upload_date TIMESTAMP
);


CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    image_name VARCHAR(255) NOT NULL,
    image_data BYTEA, -- For storing binary data
    upload_date TIMESTAMP
);

CREATE TABLE videos (
    video_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    video_name VARCHAR(255) NOT NULL,
    video_data BYTEA, -- For storing binary data
    upload_date TIMESTAMP
);
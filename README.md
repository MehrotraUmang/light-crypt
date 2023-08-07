# LightCrypt Project

LightCrypt is a Python project that demonstrates encryption and decryption using a combination of Elliptic Curve Cryptography (ECC) and Advanced Encryption Standard (AES) algorithms. The project includes a Streamlit web application for interacting with the encryption and decryption processes, generating sample data, and uploading files to an Amazon S3 bucket. The project aims to provide a user-friendly interface for understanding and experimenting with these cryptographic techniques.

## Overview

The LightCrypt project combines ECC and AES to provide a secure way of encrypting and decrypting messages. ECC is used to generate key pairs and establish a secure communication channel, while AES is used for symmetric encryption of the actual message. The Streamlit web application allows users to input plaintext messages, perform encryption and decryption, and save or upload files to an S3 bucket.

## Project Structure

The project consists of the following main components:

1. **streamlit_server.py**: This script contains the Streamlit web application code, including user interface elements and callback functions. It utilizes the ECCAES class for encryption and decryption operations, as well as the DataGenerator and S3FileManager classes for generating sample data and managing files in an S3 bucket.

2. **ecc_aes.py**: This module defines the ECCAES class, which encapsulates the ECC and AES encryption and decryption logic. It includes methods for key generation, message encryption, and message decryption using ECC and AES algorithms.

3. **data_generator.py**: This module defines the DataGenerator class, which is responsible for generating sample data in CSV and text formats. It uses the Faker library to create fake data for demonstration purposes.

4. **aws_s3.py**: This module defines the S3FileManager class, which provides functions for interacting with an Amazon S3 bucket. It allows users to list files, upload files, and delete files in the specified S3 bucket.

5. **requirements.txt**: This file lists the required Python packages and their versions needed to run the project. It includes libraries like Streamlit, Faker, and pycryptodome.

## Setup and Run

Follow these steps to set up and run the LightCrypt project:

1. Clone the repository to your local machine:

   ```bash
   git clone <repository_url>
   cd LightCrypt
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the required packages from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:

   ```bash
   streamlit run streamlit_server.py
   ```

5. Access the Streamlit web application in your web browser at `http://localhost:8501`.

## Usage

1. **Generate Data**: In the "Generate Data" tab, you can create sample CSV or text files with specified numbers of rows, columns, and tokens.

2. **Choose File**: In the "Choose File" tab, you can upload a file (CSV or text) and enter plaintext for encryption.

3. **Encrypt**: In the "Encrypt" tab, you can perform encryption using ECC and AES algorithms. The generated keys and encrypted message will be displayed.

4. **Cloud**: In the "Cloud" tab, you can upload files to an S3 bucket, view existing files, and delete files from the bucket.

Remember that this project is for educational purposes and should not be used for actual secure communications without proper validation and security audits.

## Important Notes

- Ensure you have AWS credentials properly configured if you intend to use the S3 upload and delete functionality.
- This project uses fake data and cryptographic techniques for demonstration purposes. Do not use it for real-world sensitive data without proper evaluation and security measures.
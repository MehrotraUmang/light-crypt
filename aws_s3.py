''' 
Example usage
# Create an instance of S3FileManager
s3_manager = S3FileManager(bucket_name=S3_BUCKET_NAME)

# List files in the S3 bucket
files_list = s3_manager.list_files_in_bucket()
st.write("Files in S3 Bucket:", files_list)

# Upload a file to the S3 bucket
file_path = 'path/to/your/file.txt'
file_name = 'file.txt'
s3_manager.upload_file_to_bucket(file_path, file_name)

# Delete a file from the S3 bucket
file_to_delete = 'file.txt'
s3_manager.delete_file_from_bucket(file_to_delete)
'''
import boto3
import time
import streamlit as st
import os

# Initialize AWS S3 client
#s3_client = boto3.client('s3')

# Set your AWS credentials (replace with your own credentials)
# AWS_ACCESS_KEY_ID = "your_access_key_id"
# AWS_SECRET_ACCESS_KEY = "your_secret_access_key"
# AWS_REGION = "us-west-1"  # Replace with your desired AWS region
# S3_BUCKET_NAME = "your_bucket_name"

# Specify the S3 bucket name
S3_BUCKET_NAME = 'lightcrypt-test-temp'

# Create 'uploads' directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Class to manage S3 file operations
class S3FileManager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    # List files in the S3 bucket
    def list_files_in_bucket(self):
        try:
            response = self.s3_client.list_objects(Bucket=self.bucket_name)
            if 'Contents' in response:
                files = [obj['Key'] for obj in response['Contents']]
                sidebar_dataframe_container = st.sidebar.empty()
                with sidebar_dataframe_container:
                    st.dataframe(files, use_container_width=True)
                return files
            else:
                st.write('No files found in the bucket.')
                return []
        except Exception as e:
            st.error(f'Error listing files in S3 bucket: {e}')
            return []

    # Upload a file to the S3 bucket
    def upload_file_to_bucket(self, file_path, file_name):
        try:
            start_time = time.time()
            self.s3_client.upload_file(file_path, self.bucket_name, file_name)
            end_time = time.time()
            upload_time = end_time - start_time
            st.success(f'File uploaded to S3 bucket: {file_name}')
            st.info(f'Time taken: {upload_time:.2f} seconds')
        except Exception as e:
            st.error(f'Error uploading file to S3: {e}')

    # Delete a file from the S3 bucket
    def delete_file_from_bucket(self, file_name):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)
            st.success(f'File deleted from S3 bucket: {file_name}')
        except Exception as e:
            st.error(f'Error deleting file from S3: {e}')
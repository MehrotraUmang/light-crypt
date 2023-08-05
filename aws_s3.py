import boto3
import time
import streamlit as st
import os
s3_client = boto3.client('s3')

# Set your AWS credentials (replace with your own credentials)
'''
AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"
AWS_REGION = "us-west-1"  # Replace with your desired AWS region
S3_BUCKET_NAME = "your_bucket_name"
'''

S3_BUCKET_NAME = 'lightcrypt-test-temp'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

def list_files_in_bucket():
    try:
        response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)
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

def upload_file_to_bucket(file_path, file_name):
    try:
        start_time = time.time()
        s3_client.upload_file(file_path, S3_BUCKET_NAME, file_name)
        end_time = time.time()
        upload_time = end_time - start_time
        st.success(f'File uploaded to S3 bucket: {file_name}')
        st.info(f'Time taken: {upload_time:.2f} seconds')
    except Exception as e:
        st.error(f'Error uploading file to S3: {e}')

def delete_file_from_bucket(file_name):
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)
        st.success(f'File deleted from S3 bucket: {file_name}')
    except Exception as e:
        st.error(f'Error deleting file from S3: {e}')
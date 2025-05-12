import boto3
import os
from botocore.exceptions import ClientError

# --- Configuration ---
# IMPORTANT: Storing credentials directly in code is NOT recommended for production environments.
# Consider using environment variables, AWS credentials file, or IAM roles for better security.
AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'  # Replace with your Access Key ID
AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY' # Replace with your Secret Access Key
AWS_REGION = 'your-aws-region' # Replace with your desired AWS region (e.g., 'us-east-1')

BUCKET_NAME = 'student-yourname-backup' # Replace 'yourname' with your actual name
LOCAL_FOLDER = 'daily_documents'
# --- End Configuration ---

def create_local_folder(folder_path):
    """Creates the local folder if it doesn't exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created local folder: {folder_path}")
    else:
        print(f"Local folder already exists: {folder_path}")

def create_dummy_files(folder_path, num_files=3):
    """Creates dummy text files in the specified folder."""
    if not os.listdir(folder_path): # Only create if folder is empty
        print(f"Creating {num_files} dummy files in {folder_path}...")
        for i in range(num_files):
            file_name = f"document_{i+1}.txt"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as f:
                f.write(f"This is the content of {file_name}\n")
            print(f"  Created: {file_name}")
    else:
        print(f"Dummy files already exist in {folder_path}. Skipping creation.")


def create_bucket_if_not_exists(s3_client, bucket_name, region):
    """Checks if the S3 bucket exists and creates it if it doesn't."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        # If a ClientError is thrown, then check if it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Bucket '{bucket_name}' does not exist. Creating...")
            try:
                # Specify the region for bucket creation
                if region == 'us-east-1':
                     s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                print(f"Bucket '{bucket_name}' created successfully.")
            except ClientError as create_error:
                print(f"Error creating bucket '{bucket_name}': {create_error}")
                exit(1) # Exit if bucket creation fails
        else:
            print(f"Error checking bucket '{bucket_name}': {e}")
            exit(1) # Exit on other ClientErrors

def upload_files_to_s3(s3_client, local_folder, bucket_name):
    """Uploads files from the local folder to the S3 bucket."""
    print(f"\nUploading files from '{local_folder}' to bucket '{bucket_name}'...")
    try:
        for item_name in os.listdir(local_folder):
            local_path = os.path.join(local_folder, item_name)

            # Check if the item is a file (not a directory)
            if os.path.isfile(local_path):
                s3_object_key = item_name # Use the filename as the S3 object key

                try:
                    s3_client.upload_file(local_path, bucket_name, s3_object_key)
                    print(f"Uploaded: {item_name}")
                except ClientError as upload_error:
                    print(f"Error uploading '{item_name}': {upload_error}")

    except FileNotFoundError:
        print(f"Error: Local folder '{local_folder}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    # Create the local folder and dummy files
    create_local_folder(LOCAL_FOLDER)
    create_dummy_files(LOCAL_FOLDER)

    # Initialize S3 client
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
    except Exception as e:
        print(f"Error initializing S3 client: {e}")
        exit(1)

    # Create the bucket if it doesn't exist
    create_bucket_if_not_exists(s3, BUCKET_NAME, AWS_REGION)

    # Upload the files
    upload_files_to_s3(s3, LOCAL_FOLDER, BUCKET_NAME)

    print("\nScript finished.")
    print("All operations completed successfully.")
    print("You can now check your S3 bucket for the uploaded files.")

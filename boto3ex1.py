
import os
import getpass
import subprocess
import sys
import boto3
from botocore.exceptions import ClientError
# Check for required dependencies
def configure_aws_credentials():
    try:
        # Prompt for AWS credentials
        access_key = getpass.getpass("Enter AWS Access Key ID: ")
        secret_key = getpass.getpass("Enter AWS Secret Access Key: ")
        session_token = getpass.getpass("Enter AWS Session Token (if applicable, press Enter to skip): ")
        region = input("Enter AWS Region (e.g., us-east-1): ")
        # Validate inputs
        if not access_key or not secret_key or not region:
            print("Error: Access Key ID, Secret Access Key, and Region are required.")
            return False
        # Configure AWS CLI
        subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', access_key], check=True)
        subprocess.run(['aws', 'configure', 'set', 'aws_secret_access_key', secret_key], check=True)
        
        if session_token:
            subprocess.run(['aws', 'configure', 'set', 'aws_session_token', session_token], check=True)
        
        subprocess.run(['aws', 'configure', 'set', 'region', region], check=True)
        
        print("AWS CLI credentials configured successfully!")
        return region

    except subprocess.CalledProcessError as e:
        print(f"Error configuring AWS CLI: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def manage_s3_operations(region):
    try:
        # Initialize boto3 S3 client
        s3_client = boto3.client('s3', region_name=region)

        # Define bucket name (replace 'john' with your name or a unique identifier)
        bucket_name = "student-john-bucket"  # Replace 'john' with your name or a unique identifier

        # Create the S3 bucket
        try:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
            print(f"Bucket '{bucket_name}' created successfully.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                print(f"Bucket '{bucket_name}' already exists. Proceeding with upload.")
            elif e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(f"Bucket '{bucket_name}' already owned by you. Proceeding with upload.")
            else:
                raise e

        # Upload the file team_image.png
        file_path = "team_image.png"  # Ensure this file exists in the script's directory
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found. Please ensure 'team_image.png' exists.")
            return

        s3_client.upload_file(file_path, bucket_name, "team_image.png")
        print(f"File 'team_image.png' uploaded successfully to '{bucket_name}'!")  # Bonus: Success message

        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        print("\nFiles in the bucket:")
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print("No files found in the bucket.")

    except ClientError as e:
        print(f"S3 operation failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("AWS CLI Credential Configuration and S3 Operations")
    # Verify AWS CLI is installed
    try:
        subprocess.run(['aws', '--version'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: AWS CLI is not installed. Please install it: https://aws.amazon.com/cli/")
        sys.exit(1)

    region = configure_aws_credentials()
    if region:
        manage_s3_operations(region)
    else:
        print("Failed to configure AWS credentials. S3 operations aborted.")
        print("Please ensure valid AWS credentials and try again.")
    
    # Final summary
    print("\nOperation Summary:")
    if region:
        print("- AWS CLI credentials configured.")
        print("- S3 operations attempted (check above for details).")
    else:
        print("- AWS CLI credential configuration failed.")
    
    # Optional cleanup prompt
    cleanup = input("\nWould you like to clean up (delete the uploaded file and bucket)? (y/n): ").lower()
    if cleanup == 'y' and region:
        try:
            s3_client = boto3.client('s3', region_name=region)
            bucket_name = "student-john-bucket"  # Must match the bucket name used above
            # Delete the file
            s3_client.delete_object(Bucket=bucket_name, Key="team_image.png")
            print(f"File 'team_image.png' deleted from '{bucket_name}'.")
            # Delete the bucket (must be empty)
            s3_client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deleted.")
        except ClientError as e:
            print(f"Cleanup failed: {e}")
            print("Ensure the bucket is empty and you have permissions to delete it.")
        except Exception as e:
            print(f"An unexpected error occurred during cleanup: {e}")
    elif cleanup == 'y':
        print("Cleanup skipped: No valid region provided.")
    else:
        print("Cleanup skipped: Resources remain in S3.")

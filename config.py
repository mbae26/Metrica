import os
import logging
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Load environment variables and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# AWS S3 configuration
S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=os.environ('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ('AWS_SECRET_ACCESS_KEY')
)

# AWS S3 bucket name
REQUEST_BUCKET_NAME = os.environ('REQUEST_BUCKET_NAME')

class S3Client:
    """
    Class to interact with AWS S3 for file operations.
    """

    def __init__(self, s3_client, bucket_name):
        """
        Initializes the S3Client with a boto3 client and bucket name.
        """
        self.client = s3_client
        self.bucket_name = bucket_name

    def file_exists(self, file_name):
        """
        Checks if a file exists in the S3 bucket.

        Args:
            file_name (str): The name of the file to check.

        Returns:
            bool: True if file exists, False otherwise.
        """
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=file_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                logging.error("Error checking if file %s exists in S3 bucket %s: %s",
                            file_name, self.bucket_name, e)
                raise

    def upload_file(self, file, file_name):
        """
        Uploads a file to the S3 bucket.

        Args:
            file: The file object to upload.
            file_name (str): The name of the file in the bucket.
        """
        try:
            if not self.file_exists(file_name):
                self.client.upload_fileobj(file, self.bucket_name, file_name)
                logging.info("Uploaded file %s to S3 bucket %s", file_name, self.bucket_name)
            else:
                logging.warning("File %s already exists in S3 bucket %s",
                                file_name, self.bucket_name)
        except Exception as e:
            logging.error("Error uploading file %s to S3 bucket %s: %s",
                        file_name, self.bucket_name, e)
            raise

    def download_file(self, file_name, local_path):
        """
        Downloads a file from the S3 bucket.

        Args:
            file_name (str): The name of the file in the bucket.
            local_path (str): The local path where the file will be saved.
        """
        try:
            self.client.download_file(self.bucket_name, file_name, local_path)
            logging.info("Downloaded file %s from S3 bucket %s", file_name, self.bucket_name)
        except Exception as e:
            logging.error("Error downloading file %s from S3 bucket %s: %s",
                        file_name, self.bucket_name, e)
            raise

    def delete_file(self, file_name):
        """
        Deletes a file from the S3 bucket.

        Args:
            file_name (str): The name of the file to delete.
        """
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_name)
            logging.info("Deleted file %s from S3 bucket %s", file_name, self.bucket_name)
        except Exception as e:
            logging.error("Error deleting file %s from S3 bucket %s: %s",
                        file_name, self.bucket_name, e)
            raise

import logging

from botocore.exceptions import ClientError


class S3Client:
    def __init__(self, s3_client, bucket_name):
        self.client = s3_client 
        self.bucket_name = bucket_name

    def file_exists(self, file_name):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=file_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                logging.error("Error checking if file %s exists in S3 bucket %s", file_name, self.bucket_name)
                raise
    
    def upload_file(self, file, file_name):
        try:
            if not self.file_exists(file_name):
                self.client.upload_fileobj(file, self.bucket_name, file_name)
                logging.info("Uploaded file %s to S3 bucket %s", file_name, self.bucket_name)
            else:
                logging.info("File %s already exists in S3 bucket %s", file_name, self.bucket_name)
        except:
            logging.error("Error uploading file %s to S3 bucket %s", file_name, self.bucket_name)
            raise
        
    def download_file(self, file_name, local_path):
        try:
            self.client.download_file(self.bucket_name, file_name, local_path)
            logging.info("Downloaded file %s from S3 bucket %s", file_name, self.bucket_name)
        except:
            logging.error("Error downloading file %s from S3 bucket %s", file_name, self.bucket_name)
            raise
    
    def delete_file(self, file_name):
        try:
            self.client.delete_object(self.bucket_name, file_name)
            logging.info("Deleted file %s from S3 bucket %s", file_name, self.bucket_name)
        except:
            logging.error("Error deleting file %s from S3 bucket %s", file_name, self.bucket_name)
            raise
import logging


class S3Client:
    def __init__(self, s3_client, bucket_name):
        self.client = s3_client 
        self.bucket_name = bucket_name
    
    def upload_file(self, file, file_name):
        try:
            self.client.upload_fileobj(file, self.bucket_name, file_name)
            logging.info("Uploaded file %s to S3 bucket %s", file_name, self.bucket_name)
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

    def get_file(self, file_name):
        try:
            obj = self.client.get_object(self.bucket_name, file_name)
            logging.info("Got file %s from S3 bucket %s", file_name, self.bucket_name)
            return obj
        except:
            logging.error("Error getting file %s from S3 bucket %s", file_name, self.bucket_name)
            raise
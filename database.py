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

    def download_model(self, model_path):
        local_path = f"downloads/model/{model_path}"
        try:
            self.client.download_file(self.bucket_name, model_path, local_path)
            logging.info("Downloaded model %s from S3 bucket %s", model_path, self.bucket_name)
            return local_path
        except:
            logging.error("Error downloading model %s from S3 bucket %s", model_path, self.bucket_name)
            raise
    
    def download_train_set(self, train_path):
        local_path = f"downloads/train/{train_path}"
        try:
            self.client.download_file(self.bucket_name, train_path, local_path)
            logging.info("Downloaded train set %s from S3 bucket %s", train_path, self.bucket_name)
            return local_path
        except:
            logging.error("Error downloading train set %s from S3 bucket %s", train_path, self.bucket_name)
            raise
    
    def download_test_set(self, test_path):
        local_path = f"downloads/test/{test_path}"
        try:
            self.client.download_file(self.bucket_name, test_path, local_path)
            logging.info("Downloaded test set %s from S3 bucket %s", test_path, self.bucket_name)
            return local_path
        except:
            logging.error("Error downloading test set %s from S3 bucket %s", test_path, self.bucket_name)
            raise
import os

from dotenv import load_dotenv
import boto3

import database
from s3_client import S3Client
from ml_training.process_request import RequestProcessor

load_dotenv()

s3_bucket_name = os.getenv('REQUEST_BUCKET_NAME')


def main():
    # Initialize S3 client
    s3_client_boto = boto3.client('s3',
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    s3_client = S3Client(s3_client_boto, s3_bucket_name)

    # Process each pending request
    pending_requests = database.get_pending_requests()
    for request in pending_requests:
        try:
            processor = RequestProcessor(request, s3_client, 'path_to_save_models')
            results = processor.process_request()
            print(f"Processed Request {request.id}: {results}")
            # Update the request status as COMPLETED in the database
            database.update_request_status(request.id, 'COMPLETED')
        except Exception as e:
            print(f"Failed to process Request {request.id}: {e}")
            database.update_request_status(request.id, 'FAILED')


if __name__ == '__main__':
    pass
import os

from dotenv import load_dotenv
import boto3

import database
from s3_client import S3Client
from train_eval_backend.process_request import RequestProcessor
from train_eval_backend.visualization import ModelVisualizer
from utils import ensure_directory_exists

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
    print("HERE")
    for request in pending_requests:
        try:
            ensure_directory_exists(request.user_id)
            processor = RequestProcessor(request, s3_client)
            results = processor.process_request()
            # Pass 'results' as an input to plot/visualization pipeline
            save_path = os.path.join(request.user_id, 'visual')
            ensure_directory_exists(save_path)
            visualizer = ModelVisualizer(save_path)
            visualizer.create_visualizations(results)
            
            # Create a new Result object and add it to the database
            
            # Also, process the results to send it to the user via email
            # print(f"Processed Request {request.user_id}: {results}")
            # Update the request status as COMPLETED in the database
            # database.update_request_status(request.user_id, 'COMPLETED')
        except Exception as e:
            print(f"Failed to process Request {request.user_id}: {e}")
            # database.update_request_status(request.user_id, 'FAILED')


if __name__ == '__main__':
    main()
import os
import logging
from dotenv import load_dotenv
import boto3

import app.data_management.database as database
from app.model_evaluation.process_request import RequestProcessor
from app.model_evaluation.visualization import ModelVisualizer
import app.utils as utils
from config import S3Client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize S3 client
    s3_bucket_name = os.getenv('REQUEST_BUCKET_NAME')
    s3_client_boto = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    s3_client = S3Client(s3_client_boto, s3_bucket_name)

    # Process each pending request
    try:
        pending_requests = database.get_pending_requests()
        for request in pending_requests:
            try:
                user_directory = os.path.join('data', request.user_id)
                utils.ensure_directory_exists(user_directory)

                processor = RequestProcessor(request, s3_client, user_directory)
                results = processor.process_request()

                save_path = os.path.join(user_directory, 'visuals')
                utils.ensure_directory_exists(save_path)

                visualizer = ModelVisualizer(save_path)
                visualizer.create_visualizations(results)
                visualizer.create_latex_report(results)

                # database.add_result(request.user_id, request.task_type, results)
                # utils.send_email(save_path, request.email)
                # database.update_request_status(request.user_id, 'COMPLETED')

            except Exception as e:
                logging.error("Failed to process Request %s: %s", request.user_id, e)
                # Uncomment when database operations are ready
                # database.update_request_status(request.user_id, 'FAILED')

    except Exception as e:
        logging.error("Error fetching pending requests: %s", e)

if __name__ == '__main__':
    main()

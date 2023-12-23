import os
import logging
from datetime import datetime
from dotenv import load_dotenv

import boto3
from flask import Flask, request, render_template

from s3_client import S3Client
import database

load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s')

# AWS S3 configuration
s3_client = boto3.client('s3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

# AWS S3 bucket name
request_bucket_name = os.getenv('REQUEST_BUCKET_NAME')


@app.route('/')
def index():
    return render_template('upload_form.html')


@app.route('/submit', methods=['POST'])
def upload_file():
    try:
        email = request.form['email']
        task_type = request.form['task_type']
        files = {
            'model': request.files.get('file'),
            'train': request.files.get('train_set'),
            'test': request.files.get('test_set')
        }

        user_id = email.split('@')[0]
        submission_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
        # Validate file types
        if not files['model'] or not files['model'].filename.endswith('.joblib'):
            return "Please upload a joblib file for the model"
        if not all(file.filename.endswith('.csv') for file in [files['train'], files['test']]):
            return "Please upload csv files for the training and test sets"

        client = S3Client(s3_client, request_bucket_name)

        for file_type, file in files.items():
            s3_file_path = f"{file_type}/{user_id}_{submission_time}"
            client.upload_file(file, s3_file_path)
            logging.info("Uploaded file %s to S3 bucket %s", s3_file_path, request_bucket_name)
        
        database.add_request(user_id, submission_time, task_type)
        logging.info(f"Model submitted successfully. Request ID: {user_id}")

        return "Model submitted successfully"
    
    except Exception as e:
        logging.error("Error in upload_file function: %s", e)
        return "An error occurred while submitting the model"

if __name__ == '__main__':
    app.run(debug=True)
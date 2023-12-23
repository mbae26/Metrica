import os
import logging
from datetime import datetime
from dotenv import load_dotenv

import boto3
from flask import Flask, request, render_template

import utils

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


@app.route('/Submit', methods=['POST'])
def upload_file():
    email = request.form['email']
    task_type = request.form['task_type']
    train_file = request.files['train_set']
    test_file = request.files['test_set']
    model_file = request.files['file']
    
    if not model_file or not model_file.filename.endswith('.joblib'):
        return "Please upload a joblib file"

    submission_time = datetime.now().strftime("%Y%m%d%H%M%S")
    user_id = email.split('@')[0]  # using the part before '@' as UserID
    
    request_obj = utils.Request(user_id, submission_time, task_type=task_type)

    # Process and upload each model, train, and test file to S3 bucket
    s3_file_paths = request_obj.get_file_names()
    
    for file_type, s3_file_path in s3_file_paths.items():
        if file_type == 'model':
            file = model_file
        elif file_type == 'train':
            file = train_file
        else:
            file = test_file
        
        if file:
            s3_client.upload_fileobj(file, request_bucket_name, s3_file_path)
            logging.info("User %s uploaded %s file at %s", user_id, file_type, submission_time)
            
    # Log the request
    request_obj.log_request()
    
    return "Model submitted successfully"


if __name__ == '__main__':
    app.run(debug=True)

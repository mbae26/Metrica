import os
import logging
from datetime import datetime
from dotenv import load_dotenv

import boto3
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import utils

load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='submission_log.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# AWS S3 configuration
s3_client = boto3.client('s3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

# AWS S3 bucket name
bucket_name = os.getenv('REQUEST_BUCKET_NAME')

@app.route('/')
def index():
    return render_template('upload_form.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.form['user_id']
    file = request.files['file']
    
    if not file or not file.filename.endswith('.joblib'):
        return_msg = "Please upload a joblib file"
        return return_msg

    filename = secure_filename(file.filename)
    submission_time = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_file_path = f"{user_id}/{submission_time}/{filename}.joblib"     # double check "file path"

    # Upload file to S3 bucket
    s3_client.upload_fileobj(file, bucket_name, s3_file_path)
    
    # Log the request to 
    logging.info(f"User {user_id} uploaded file {filename} at {submission_time}")
    # Log the request to a JSON file
    request_data = {
        'user_id': user_id, 
        'submission_time': submission_time,
        'status': 'PENDING',    # Consider using an enum for this 
    }
    # utils.write_to_json(request_data)
    
    # Return success message
    return_msg = f"File {filename} uploaded successfully"
    return return_msg




if __name__ == '__main__':
    app.run(debug=True)

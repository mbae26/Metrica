import os
import hashlib
from datetime import datetime
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app as app
from config import S3_CLIENT, REQUEST_BUCKET_NAME, S3Client
from app.data_management import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_directory_exists(path):
    """
    Creates a directory if it does not exist.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logging.error("Error creating directory %s: %s", path, e)
        raise


def send_email(receiver_email, results, task_type, attachments=None):
    """
    Sends an email with the results and optional attachments.
    """
    try:
        sender_email = app.config['SENDER_EMAIL']
        password = app.config['SENDER_EMAIL_PASSWORD']

        subject = "Model Processing Results"
        email_body = "Your model processing is completed. Please find the results attached."

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(email_body, 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as file:
                    part = MIMEText(file.read(), 'base64')
                    part.add_header('Content-Disposition', 
                                    'attachment; filename="{}"'.format(os.path.basename(attachment)))
                    message.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error("Error in sending email: %s", e)


def upload_file_logic(request):
    try:
        email = request.form['email'].lower()
        task_type = request.form['task_type'].lower()
        submission_time = datetime.now().strftime("%Y%m%d%H%M%S")

        unique_id_string = f"{email}_{submission_time}"
        # Create a hash of email and submission time to generate a unique ID
        user_id = hashlib.sha256(unique_id_string.encode()).hexdigest()
        logging.info("Unique ID generated for the request: %s", user_id)

        files = {
            'model': request.files.get('model'),
            'train': request.files.get('train_set'),
            'test': request.files.get('test_set')
        }

        # Validate file types
        if not files['model'] or not files['model'].filename.endswith('.joblib'):
            return "Please upload a joblib file for the model"
        if not all(file.filename.endswith('.csv') for file in [files['train'], files['test']]):
            return "Please upload csv files for the training and test sets"

        client = S3Client(S3_CLIENT, REQUEST_BUCKET_NAME)

        for file_type, file in files.items():
            s3_file_path = f"{user_id}_{file_type}"
            client.upload_file(file, s3_file_path)

        database.add_request(user_id, email, submission_time, task_type)
        logging.info("Model submitted successfully. Request ID: %s", user_id)

        return "Model submitted successfully"

    except Exception as e:
        logging.error("Error in upload_file function: %s", e)
        return "An error occurred while submitting the model"

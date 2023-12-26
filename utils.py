import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def ensure_directory_exists(path):
    """
    Creates a directory if it does not exist.

    Args:
        path (str): Path to the directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def send_email(receiver_email, results, task_type, attachments=None):
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_EMAIL_PASSWORD')
    
    # Create an email message
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
    
    # Create secure connection with server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        text.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error in sending email: {e}")


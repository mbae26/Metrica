import json
import logging


class RequestLogger:
    def __init__(self, log_file='requests.json'):
        self.log_file = log_file
    
    def log_request(self, request_data):
        with open(self.log_file, 'a') as f:
            f.write(request_data.to_json() + '\n')
            logging.info("Logged request for user %s", request_data.user_id)


class Request:
    def __init__(self, user_id, submission_time, status="PENDING", task_type="CLASSIFICATION"):
        self.user_id = user_id
        self.submission_time = submission_time
        self.status = status
        self.task_type = task_type

    def __repr__(self):
        return (f"Request(user_id={self.user_id}, submission_time={self.submission_time}, "
                f"status={self.status}, task_type={self.task_type})")

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'submission_time': self.submission_time,
            'status': self.status,
            'task_type': self.task_type
        }

    def get_file_paths(self):
        base_path = f"{self.user_id}_{self.submission_time}_"
        return {
            'model': base_path + "model",
            'train': base_path + "train",
            'test': base_path + "test"
        }


# Utility functions for handling requests
def fetch_latest_request(log_file='requests.json'):
    try:
        requests = read_requests(log_file)
        return next((req for req in requests if req['status'] == 'PENDING'), None)
    except Exception as e:
        logging.error(f"Error fetching latest request: {e}")
        return None


def read_requests(log_file):
    with open(log_file, 'r') as f:
        return [json.loads(line) for line in f]
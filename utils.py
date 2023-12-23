import json
import logging

class Request:
    def __init__(self, user_id, submission_time, status="PENDING", task_type="CLASSIFICATION"):
        self.user_id = user_id
        self.submission_time = submission_time
        self.status = status
        self.task_type = task_type
    
    def __repr__(self):
        return f"Request(user_id={self.user_id}, submission_time={self.submission_time}, status={self.status}, task_type={self.task_type})"
    
    def to_json(self):
        return json.dumps(self)
    
    def get_file_names(self):
        model_file_name = f"model/{self.user_id}_{self.submission_time}"
        train_file_name = f"train/{self.user_id}_{self.submission_time}"
        test_file_name = f"test/{self.user_id}_{self.submission_time}"
        
        file_names = {'model': model_file_name, 'train': train_file_name, 'test': test_file_name}
        return file_names
        
    def log_request(self):
        with open('requests.json', 'a') as f:
            f.write(self.to_json() + '\n')
            logging.info("Logged request for user %s", self.user_id)


def fetch_latest_request():
    try:
        requests = read_requests()
        pending_request = find_pending_request(requests)
        
        if not pending_request:
            logging.info("No pending requests found")
            return None
        return pending_request
    except Exception as e:
        return None
        

def read_requests():
    with open('requests.json', 'r') as f:
        return [json.loads(line) for line in f]

def find_pending_request(requests):
    for request in requests:
        if request['status'] == 'PENDING':
            return request
    return None

def download_file_from_s3(s3_client, bucket_name, request):
    user_id = request['user_id']
    submission_time = request['submission_time']
    file_type = request['task_type']
    
    for file_type in ['model', 'train', 'test']:
        file_path = f"{user_id}_{submission_time}_{file_type}"
        s3_client.download_file(bucket_name, file_path, "downloads/{file_path}")
        logging.info("Downloaded %s file for user %s", file_type, user_id)
    

def write_requests_to_json(request_data):
    with open('requests.json', 'a') as f:
        json.dump(request_data, f)
        f.write('\n')

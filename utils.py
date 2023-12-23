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
    
    def to_json(self):
        return json.dumps(self.to_dict())


class RequestQueue:
    def __init__(self, queue_file='request_queue.json'):
        self.queue_file = queue_file
    
    def add_request(self, request):
        with open(self.queue_file, 'a') as f:
            f.write(request.to_json() + '\n')
            logging.info("Added request for user %s to queue", request.user_id)
    
    def get_next_request(self):
        with open(self.queue_file, 'r') as f:
            requests = [json.loads(line) for line in f]
        pending_requests = [req for req in requests if req['status'] == 'PENDING']
        return pending_requests[0] if pending_requests else None
    
    def update_request_status(self, request, status):
        with open(self.queue_file, 'r') as f:
            requests = [json.loads(line) for line in f]
        for req in requests:
            if req['user_id'] == request.user_id and req['submission_time'] == request.submission_time:
                req['status'] = status
                break
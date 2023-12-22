import json
import logging

def read_requests():
    with open('requests.json', 'r') as f:
        return [json.loads(line) for line in f]

def find_pending_request(requests):
    pass

def update_request_status():
    pass

def download_file_from_s3():
    pass

def write_requests_to_json():
    pass

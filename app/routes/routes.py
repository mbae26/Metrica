from flask import Blueprint, render_template, request
import app.utils as utils

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['GET'])
def submit():
    return render_template('submission.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    return utils.upload_file_logic(request)

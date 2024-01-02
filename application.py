from flask import Flask, render_template, request
import app.utils as utils

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/submit', methods=['GET'])
def submit():
    return render_template('submission.html')

@application.route('/upload', methods=['POST'])
def upload_file():
    return utils.upload_file_logic(request)

if __name__ == "__main__":
    application.run(debug=True)
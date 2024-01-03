from flask import Flask, render_template, request
import app.utils as utils

application = Flask(__name__)

if __name__ == "__main__":
    application.run(debug=True)

from flask import Flask
from app.routes.routes import main as main_blueprint

def create_app():
    application = Flask(__name__)
    application.register_blueprint(main_blueprint)
    return application
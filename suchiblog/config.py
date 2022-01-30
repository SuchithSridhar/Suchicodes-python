import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    RESOURCES_DIR = 'data'
    PROJECTS_UPLOAD_FOLDER = './suchiblog/static/uploaded-data'
    NOTIFY_KEY = os.environ.get('FLASK_NOTIFY_KEY')
    MESSAGE_FILE = './suchiblog/data/message-data.json'

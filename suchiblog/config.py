import os

class Config:
    SECRET_KEY = os.environ.get('SUCHICODES_SECRET_KEY')
    SUCHICODES_ENV = os.environ.get('SUCHICODES_ENV') if os.environ.get('SUCHICODES_ENV') else 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESOURCES_DIR = 'data'
    PROJECTS_UPLOAD_FOLDER = './suchiblog/static/uploaded-data'
    NOTIFY_KEY = os.environ.get('FLASK_NOTIFY_KEY')
    MESSAGE_FILE = './suchiblog/data/message-data.json'
    IP_LOGS_FILE_BASE = './suchiblog/data/ip-logs-csv-{}.csv'

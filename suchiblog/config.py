import os


class Config:
    SECRET_KEY = os.environ.get('SUCHICODES_SECRET_KEY')
    SUCHICODES_ENV = \
        os.environ.get('SUCHICODES_ENV') if os.environ.get('SUCHICODES_ENV') \
        else 'development'
    SUCHI_SERVER_PASS_HASH = os.environ.get('SUCHI_SERVER_PASS_HASH')
    SUCHI_SERVER_CHECKIN_FILE = os.environ.get('SUCHI_SERVER_CHECKIN_FILE')
    SUCHI_SERVER_VAIDATION = os.environ.get('SUCHI_SERVER_VALIDATION')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESOURCES_DIR = 'data'
    PROJECTS_UPLOAD_FOLDER = './suchiblog/static/uploaded-data'
    NOTIFY_KEY = os.environ.get('SUCHICODES_NOTIFY_KEY')
    NOTIFY_URL = f"https://maker.ifttt.com/trigger"\
                 f"/notify/with/key/{NOTIFY_KEY}"
    MESSAGE_FILE = './suchiblog/data/message-data.json'
    IP_BLACKLIST = './suchiblog/config/ip_blacklist'
    MESSAGE_BLACKLIST = './suchiblog/config/message_blacklist'
    DATETIME_COMPLETE_FORMAT = "%Y-%m-%d_%H-%M-%S"
    DELETED_CATEGORY_ID = 999999
    NOTES_CONFIG_FILENAME = 'suchicodes-config.json'
    UPLOAD_DIR_URL = "/static/uploaded-data"

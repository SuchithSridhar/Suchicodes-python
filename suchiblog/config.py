import os
import datetime


def value_or_default(item1, item2):
    if item1 is not None and item1 != "":
        return item1
    else:
        return item2


class Config:
    SECRET_KEY = os.environ.get('SUCHICODES_SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
    SUCHICODES_ENV = value_or_default(
        os.environ.get('SUCHICODES_ENV'), "development"
    )
    SECRET_PASS_HASH = os.environ.get('SECRET_PASS_HASH')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESOURCES_DIR = 'data'
    PROJECTS_UPLOAD_FOLDER = './suchiblog/static/uploaded-data'
    NOTIFY_URL = os.environ.get('SUCHICODES_NOTIFY_URL')
    MESSAGE_FILE = './suchiblog/data/message-data.json'
    IP_BLACKLIST = './suchiblog/config/ip_blacklist'
    MESSAGE_BLACKLIST = './suchiblog/config/message_blacklist'
    DATETIME_COMPLETE_FORMAT = "%Y-%m-%d_%H-%M-%S"
    DELETED_CATEGORY_ID = 999999
    NOTES_CONFIG_FILENAME = 'suchicodes-config.json'
    UPLOAD_DIR_URL = "/static/uploaded-data"

    LOGGING_FORMAT = "%(asctime)s :: %(levelname)s :: %(message)s"
    LOGGING_FILE = "suchiblog/logs/logs.log"
    INTERNAL_USER = "internal"

    ASTRAX_SERVER_TAG = "astrax"
    BERNUM_SERVER_TAG = "bernum"
    SERVER_CHECKIN_TAG = "server-checkin"
    SERVER_OFFLINE_TAG = "server-offline"
    AVAILABLE_SERVER_COMMANDS = ['restart', 'ssh-restart']
    CHECKIN_LIMIT = 5  # Number of logs kept for each server
    THRESHOLD_MINS = 10  # Mins before server marked as offline

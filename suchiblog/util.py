import hashlib
import base64
import yaml
import json
import uuid
import datetime
import requests
from .config import Config

class Util:
    def hash_password(password):
        hasher = hashlib.sha512()
        hasher.update(password.encode())
        return base64.urlsafe_b64encode(hasher.digest())

    def get_locale_data(lang="en"):
        stream = open(f'suchiblog/config/locales/{lang}.yml')
        data = yaml.load(stream, Loader=yaml.Loader)
        data = {'ln': data}
        return data

    def get_skill_list():
        try:
            data = open('suchiblog/data/skills.json').read()
            data = json.loads(data)
        except FileNotFoundError:
            data = {}
        
        return data

    def create_uuid():
        return str(uuid.uuid4())

    def log_contact_message(subject, message):
        d = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        complete_message = f"{d}:\n{subject}\n{message}\n\n"
        with open(Config.MESSAGE_FILE, 'a') as f:
            f.write(complete_message)

        url = f"https://maker.ifttt.com/trigger/notify/with/key/{Config.NOTIFY_KEY}"
        data = {
            'value1': f"{d}:\n{subject}\n{message}"[:50]
        }
        requests.post(url, data=data)


        
        
import hashlib
import base64
import yaml
import json
import uuid
import datetime
import requests
import threading
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

    def log_contact_message(subject, message, ip):
        d = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        try:
            json_data = json.loads(open(Config.MESSAGE_FILE).read())
        except FileNotFoundError:
            json_data = {}
        json_data[d] = {
            'IP': ip,
            'Subject': subject,
            'Message': message
        }
        with open(Config.MESSAGE_FILE, 'w') as f:
            f.write(json.dumps(json_data))

        url = f"https://maker.ifttt.com/trigger/notify/with/key/{Config.NOTIFY_KEY}"
        data = {
            'value1': f"New message on suchicodes.com"
        }
        requests.post(url, data=data)

    def log_ip_access_process(ip, date, url, db, app, ip_logs):
        item = ip_logs(ip=ip, url=url, date=date)
        with app.app_context():
            db.session.add(item)
            db.session.commit()

    def log_ip_access(ip, url, db, app, IP_Logs):
        date=datetime.datetime.now()
        threading.Thread(target=Util.log_ip_access_process, name='log-ip', args=[
            ip,
            date,
            url,
            db,
            app,
            IP_Logs
        ]).start()

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

    def get_pre_render_data(flask, lang="en"):
        stream = open(f'suchiblog/config/locales/{lang}.yml')
        lang = yaml.load(stream, Loader=yaml.Loader)
        if flask is None:
            mode = 'light'
        else:
            mode = f'{flask.session.get("value")}'

        data = {
            'ln': lang,
            'mode': mode
        }
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
        ignore_ips = [
                '77.51.27.234'
        ]

        for i in ignore_ips:
            if str(ip) == i:
                return None


        try:
            json_data = json.loads(open(Config.MESSAGE_FILE).read())
        except FileNotFoundError:
            json_data = {}
        json_data[d] = {
            'IP': ip,
            'Subject': subject,
            'Message': message
        }
        with open(Config.MESSAGE_FILE, 'w') as fin:
            fin.write(json.dumps(json_data))

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
        ignore = [
            '/session/get',
            'suchicodes.com/admin',
            '/session/set/dark',
            '/session/set/light',
            '.css',
            '.js',
            '.ico',
            '.svg',
            '.gif',
            '.mp4',
            '.png'
        ]

        ignore_ips = [
                '77.51.27.234'
        ]

        for i in ignore:
            if i in url:
                return None

        for i in ignore_ips:
            if str(ip) == i:
                return None

        date=datetime.datetime.now()
        threading.Thread(target=Util.log_ip_access_process, name='log-ip', args=[
            ip,
            date,
            url,
            db,
            app,
            IP_Logs
        ]).start()

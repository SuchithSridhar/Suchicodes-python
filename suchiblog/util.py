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
    @staticmethod
    def hash_password(password: str):
        hasher = hashlib.sha512()
        hasher.update(password.encode())
        return base64.urlsafe_b64encode(hasher.digest()).decode('UTF-8')

    @staticmethod
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

    @staticmethod
    def get_skill_list():
        try:
            data = open('suchiblog/data/skills.json').read()
            data = json.loads(data)
        except FileNotFoundError:
            data = {}

        return data

    @staticmethod
    def create_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def send_notification(title: str, message: str, priority: int = 9) -> bool:
        url = Config.NOTIFY_URL
        if (url is None):
            return False

        data = {'title': title, 'message': message, 'priority': str(priority)}

        requests.post(url, data=data, verify=True)
        return True

    @staticmethod
    def log_contact_message(subject, message, ip, app, db, ContactModel):
        d = datetime.datetime.now()

        item = ContactModel(
            date=d,
            subject=subject,
            message=message,
            ip=ip,
        )
        with app.app_context():
            db.session.add(item)
            db.session.commit()

        Util.send_notification(
            "Message on Suchicodes",
            f"{(subject+': '+message)[:100]}",
            priority=5
        )

    @staticmethod
    def log_ip_access_process(
            ip,
            other_information,
            date,
            url,
            db,
            app,
            ip_logs):
        item = ip_logs(
            ip=ip,
            url=url,
            date=date,
            sec_ch_ua=other_information.get("HTTP_SEC_CH_UA", ""),
            mobile=other_information.get("HTTP_SEC_CH_UA_MOBILE", ""),
            platform=other_information.get("HTTP_SEC_CH_UA_PLATFORM", ""),
            reference=other_information.get("HTTP_REFERER", ""),
            user_agent=other_information.get("HTTP_USER_AGENT", "")
        )
        with app.app_context():
            db.session.add(item)
            db.session.commit()

    @staticmethod
    def log_ip_access(ip, other_information, url, db, app, IP_Logs):
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

        for i in ignore:
            if i in url:
                return None

        date = datetime.datetime.now()
        threading.Thread(
            target=Util.log_ip_access_process,
            name='log-ip',
            args=[ip, other_information, date, url, db, app, IP_Logs]).start()

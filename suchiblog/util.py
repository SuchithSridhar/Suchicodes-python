import hashlib
import base64
import yaml
import json
import uuid

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
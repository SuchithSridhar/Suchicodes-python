import hashlib
import base64
import yaml

class Util:
    def hash_password(password):
        hasher = hashlib.sha512()
        hasher.update(password.encode())
        return base64.urlsafe_b64encode(hasher.digest())

    def read_locale_data(lang="en"):
        stream = open(f'suchiblog/config/locales/{lang}.yml')
        data = yaml.load(stream, Loader=yaml.Loader)
        data = {'ln': data}
        return data
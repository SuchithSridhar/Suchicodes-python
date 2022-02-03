from . import db, login_manager;
from .util import Util
import flask_login as fl


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


class Projects(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    title = db.Column(db.String)
    html = db.Column(db.Text) # This is HTML content
    markdown = db.Column(db.Text) # This is markdown content
    url = db.Column(db.String)
    brief = db.Column(db.String)
    img = db.Column(db.String)


class Category(db.Model):
    # if the parent id=0 then it's a top level category
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String)
    uuid = db.Column(db.String)


class Blog(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    date = db.Column(db.DateTime)
    title = db.Column(db.String)
    html = db.Column(db.Text) # This is HTML content
    markdown = db.Column(db.Text) # This is markdown content
    brief = db.Column(db.String)
    category = db.Column(db.String)


class IP_Logs(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    date = db.Column(db.DateTime)
    url = db.Column(db.String)
    ip = db.Column(db.String)


class User(db.Model, fl.UserMixin):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roles_string = db.Column(db.String)
    def roles(self):
        if self.roles_string is not None:
            return self.roles_string.split(',')


class Diary_Entry(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    user_id = db.Column(db.String)
    date = db.Column(db.DateTime)
    html = db.Column(db.Text) # This is HTML content
    markdown = db.Column(db.Text) # This is markdown content
from . import db, login_manager
from .util import Util
import flask_login as fl


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(str(admin_id))


class Admin(db.Model, fl.UserMixin):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<User '{self.id}': '{self.email}'>"


class Projects(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    title = db.Column(db.String)
    html = db.Column(db.Text)  # This is HTML content
    markdown = db.Column(db.Text)  # This is markdown content
    url = db.Column(db.String)
    brief = db.Column(db.String)
    img = db.Column(db.String)

    def __repr__(self):
        return f"<Project '{self.id}': '{self.title}'>"


class Category(db.Model):
    # if the parent id=0 then it's a top level category
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    blogs = db.relationship("Blog", backref="category")
    name = db.Column(db.String)
    uuid = db.Column(db.String)

    def __repr__(self):
        return f"<Category '{self.id}': '{self.name}'>"


class Blog(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    title = db.Column(db.String)
    html = db.Column(db.Text)  # This is HTML content
    markdown = db.Column(db.Text)  # This is markdown content
    brief = db.Column(db.Text)
    picture_map = db.Column(db.Text)

    def __repr__(self):
        return f"<Blog '{self.id}': '{self.title}'>"


class IP_Logs(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    date = db.Column(db.DateTime)
    url = db.Column(db.String)
    ip = db.Column(db.String)
    sec_ch_ua = db.Column(db.String)
    mobile = db.Column(db.String)
    platform = db.Column(db.String)
    reference = db.Column(db.String)
    user_agent = db.Column(db.String)

    def __repr__(self):
        return f"<IP-Log '{self.date}': '{self.ip}'>"


class Extern_Messages(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    timestamp = db.Column(db.DateTime)
    tags = db.Column(db.String)
    user = db.Column(db.String)
    message = db.Column(db.String)

    def tags_contains(self, tag: str):
        return f"#{tag}$" in self.tags

    def clean_tags(self):
        return ", ".join(self.tags_array())

    def tags_array(self):
        return list(map(lambda x: x[1:-1], self.tags.split(",")))

    @staticmethod
    def create_tags(tags: list):
        return ",".join(map(lambda item: f"#{item}$", tags))


class Contact(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    date = db.Column(db.DateTime)
    subject = db.Column(db.String)
    message = db.Column(db.String)
    ip = db.Column(db.String)

    def __repr__(self):
        return f"<Contact '{self.date}': '{self.subject}'>"


class URL_Redirection(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    keyword_in = db.Column(db.String)
    url_out = db.Column(db.String)

    def __repr__(self):
        return f"<URL-Redirect '{self.keyword_in}': '{self.url_out}'>"

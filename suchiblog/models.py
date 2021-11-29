from . import db;
from .util import Util

class Projects(db.Model):
    id = db.Column(db.String, primary_key=True, default=Util.create_uuid)
    title = db.Column(db.String)
    html = db.Column(db.Text) # This is HTML content
    markdown = db.Column(db.Text) # This is markdown content
    url = db.Column(db.String)
    brief = db.Column(db.String)
    img = db.Column(db.String)
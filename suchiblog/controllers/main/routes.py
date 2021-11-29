import flask as f
from ...util import Util

main_blueprint = f.Blueprint('main', __name__)

@main_blueprint.route("/session/get")
def get_session():
    return f'{f.session.get("value")}'

@main_blueprint.route("/session/set/<value>")
def set_session(value):
    f.session['value'] = value
    return 'Session set'

@main_blueprint.route("/")
def index():
    return f.render_template('main/index.jinja', title="Home | Suchicodes", skills=Util.get_skill_list())
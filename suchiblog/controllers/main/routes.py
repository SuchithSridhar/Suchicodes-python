import flask as f

main_blueprint = f.Blueprint('main', __name__)

@main_blueprint.route("/session/get")
def get_session():
    return f'Value set in session {f.session.get("value")}'

@main_blueprint.route("/session/set/<value>")
def set_session(value):
    f.session['value'] = value
    return 'Session set'

@main_blueprint.route("/")
def index():
    return "Set up"
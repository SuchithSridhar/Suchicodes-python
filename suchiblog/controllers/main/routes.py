import flask as f
from ...util import Util

main_blueprint = f.Blueprint('main', __name__)
contact_alert = False

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

@main_blueprint.route("/about")
def about():
    return f.render_template('main/about.jinja', title="About | Suchicodes")

@main_blueprint.route("/contact", methods=['get','post'])
def contact():
    alert = False
    if f.request.method == 'POST':
        sub = f.escape(f.request.form['subject'])
        message = f.escape(f.request.form['message'])
        Util.log_contact_message(sub, message, f.request.remote_addr)
        alert = True

    return f.render_template('main/contact.jinja', title="Contact | Suchicodes", alert=alert)

@main_blueprint.route('/resume.pdf')
@main_blueprint.route('/resume')
def send_pdf():
    return f.send_from_directory(f.current_app.config['RESOURCES_DIR'], 'resume.pdf')

@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return f.render_template('error-pages/404.jinja'), 404
import flask as f
from ...util import Util
from ...models import URL_Redirection
from ...config import Config

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

@main_blueprint.route("/url/<keyword>")
def url_redirection(keyword):
    url = URL_Redirection.query.filter_by(keyword_in=keyword).first()
    if not url:
        f.abort(404)
        return
    
    return f.redirect(url.url_out)


@main_blueprint.route("/contact", methods=['get','post'])
def contact():
    alert = False
    if f.request.method == 'POST':
        ip = f.request.environ.get('HTTP_X_REAL_IP', f.request.remote_addr)
        if ip is None:
            ip = f.request.remote_addr
        else:
            try:
                index = ip.index(',')
                ip = ip[:index]
            except ValueError:
                pass


        # Check blacklist of ip addresses

        try:
            with open(Config.IP_BLACKLIST) as fin:
                if str(ip).strip() in fin.read():
                    return "No"
        except FileNotFoundError:
            pass

        # Check blacklist of messages

        try:
            with open(Config.MESSAGE_BLACKLIST) as fin:
                for line in fin.readlines():
                    if line.strip() in message:
                        return "No"
        except FileNotFoundError:
            pass


        sub = f.escape(f.request.form['subject'])
        message = f.escape(f.request.form['message'])
        Util.log_contact_message(sub, message, ip)
        alert = True

    return f.render_template('main/contact.jinja', title="Contact | Suchicodes", alert=alert)

@main_blueprint.route('/resume.pdf')
@main_blueprint.route('/resume')
def send_pdf():
    return f.send_from_directory(f.current_app.config['RESOURCES_DIR'], 'resume.pdf')

@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return f.render_template('error-pages/404.jinja'), 404
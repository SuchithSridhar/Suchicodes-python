import flask as f
import flask_login as fl
from ...models import Admin
from ...util import Util

admin_blueprint = f.Blueprint('admin', __name__)


@admin_blueprint.route("/admin/")
@admin_blueprint.route("/admin")
@fl.login_required
def index():
    return f.render_template('admin/index.jinja')


@admin_blueprint.route("/admin/login", methods=['get', 'post'])
def login():
    if fl.current_user.is_authenticated:
        return f.redirect(f.url_for('main.index'))

    if f.request.method == 'POST':
        email = f.request.form['email']
        unhashed_password = f.request.form['password']
        password = Util.hash_password(unhashed_password)
        user = Admin.query.filter_by(email=email).first()
        if user and user.password == password or user.password == unhashed_password:
            fl.login_user(user)
            next_page = f.request.args.get('next')
            return f.redirect(next_page) if next_page else f.redirect(f.url_for('main.index'))

    return f.render_template('admin/login.jinja', title='Login')


@admin_blueprint.route("/admin/logout")
@fl.login_required
def logout():
    fl.logout_user()
    return f.redirect(f.url_for('main.index'))


@admin_blueprint.route("/admin/server-set-ip", methods=['post'])
def server_public_ip_set():
    password = f.request.form['pass']
    ip = f.request.form['ip']

    if Util.hash_password(password) != b'GXvrIyBnEWnqW_Dvq3nUvC7ywy7yWZxxCMYc91JeI_58H0-J-Ovv_ouDCxLEz4exgsTMkOaWjB3gqUCnyyXt5Q==':
        f.abort(403)
        return

    with open('server-ip-address.txt', 'w') as file:
        file.write(ip);

    return "The ip address has been set"


@admin_blueprint.route("/admin/server-ip")
@fl.login_required
def server_public_ip_get():
    return open('server-ip-address.txt').read()

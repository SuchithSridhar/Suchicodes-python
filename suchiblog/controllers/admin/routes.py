import json
import flask as f
import flask_login as fl
import datetime
from .adminUtil import re_compute_markdowns
from ...models import Admin, IP_Logs
from ...util import Util
from ...config import Config
from ... import db

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

@admin_blueprint.route("/admin/re_compute_markdowns")
@fl.login_required
def re_compute_markdowns_endpoint():
    re_compute_markdowns(f.current_app, db)
    return "Markdowns will be recomputed."


@admin_blueprint.route("/admin/messages")
@fl.login_required
def messages():
    try:
        data = json.loads(open(Config.MESSAGE_FILE).read())
    except FileNotFoundError:
        data = {}

    return f.render_template('admin/messages.jinja', title='Messages', messages=data)

@admin_blueprint.route("/admin/ip-logs")
@fl.login_required
def ip_logs():
    logs = IP_Logs.query.order_by(IP_Logs.date.desc()).paginate(per_page=20)
    return f.render_template('admin/ip-logs.jinja', title='IP-logs', logs=logs)

@admin_blueprint.route("/admin/delete-logs")
@fl.login_required
def delete_ip_logs():
    date = datetime.datetime.now().strftime('%y-%m-%d')
    with open(Config.IP_LOGS_FILE_BASE.format(date), 'a') as f:
        for log in IP_Logs.query.all():
            f.write(f"{log.date}, {log.ip}, {log.url}\n")

    try:
        num_rows_deleted = db.session.query(IP_Logs).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return "Ip logs have been deleted."
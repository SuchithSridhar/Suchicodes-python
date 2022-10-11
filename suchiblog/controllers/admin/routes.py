import json
import flask as f
import flask_login as fl
import datetime
from .adminUtil import re_compute_markdowns
from ...models import Admin, IP_Logs, URL_Redirection
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
        if user and (user.password == password or user.password == unhashed_password):
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


@admin_blueprint.route("/admin/blacklist")
@fl.login_required
def blacklist():
    block = f.request.args.get('type')

    if block == 'ip':
        ip = f.request.args.get('ip')
        with open(Config.IP_BLACKLIST) as fin:
            if ip in fin.read():
                return f"{ip} already present in the blacklist"

        with open(Config.IP_BLACKLIST, 'a') as fin:
            fin.write("\n" + ip)

        return f"{ip} has been added to the blacklist"
    
    elif block == 'message':
        message = f.request.get('message')

        with open(Config.MESSAGE_BLACKLIST) as fin:
            for line in fin.readlines():
                if message in line:
                    return f"Message already present in the blacklist"

        with open(Config.MESSAGE_BLACKLIST, 'a') as fin:
            fin.write("\n" + message)

        return "Message has been added to blacklist"



    return "Invalid type for blacklist"

@admin_blueprint.route("/admin/url-redirects", methods=['GET', 'POST'])
@fl.login_required
def url_redirects():
    if f.request.method == 'POST':
        keyword = f.request.form['keyword_in']
        url = f.request.form['url_out']
        u = URL_Redirection(keyword_in=keyword, url_out=url)
        db.session.add(u)
        db.session.commit()
        return f.redirect("/admin/url-redirects")

    if f.request.method == 'GET':
        urls = URL_Redirection.query.paginate(per_page=20)
        return f.render_template('admin/url-redirects.jinja', title='URL Redirects', urls=urls)

@admin_blueprint.route("/admin/url-redirects/delete/<id>")
@fl.login_required
def url_redirects_delete(id):
    url = URL_Redirection.query.filter_by(id=id).first()
    if not url:
        f.abort(404)
        return

    db.session.delete(url)
    db.session.commit()
    return "URL Redirect deleted."

@admin_blueprint.route("/admin/ip-logs")
@fl.login_required
def ip_logs():
    logs = IP_Logs.query.order_by(IP_Logs.date.desc()).paginate(per_page=20)
    return f.render_template('admin/ip-logs.jinja', title='IP-logs', logs=logs)

@admin_blueprint.route("/admin/delete-messages")
@fl.login_required
def delete_messages():
    date = datetime.datetime.now().strftime('%y-%m-%d')
    with open(Config.MESSAGE_FILE, 'w') as fin:
        fin.write(json.dumps({}))
    return "All messages have been deleted."

@admin_blueprint.route("/admin/delete-logs")
@fl.login_required
def delete_ip_logs():
    date = datetime.datetime.now().strftime('%y-%m-%d')
    with open(Config.IP_LOGS_FILE_BASE.format(date), 'a') as fin:
        for log in IP_Logs.query.all():
            fin.write(f"{log.date}, {log.ip}, {log.url}\n")

    try:
        num_rows_deleted = db.session.query(IP_Logs).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return "Ip logs have been deleted."

from datetime import datetime
from os import kill
import flask as f
import flask_login as fl
from .admin_util import AdminUtil
from ...models import IP_Logs, URL_Redirection, Contact, Extern_Messages
from ...util import Util
from ...config import Config
from ... import db, logger

admin_blueprint = f.Blueprint('admin', __name__)

# A way to communicate to the physical servers
# Format: "serverid: [operations]"
server_messages_queue = {
    Config.ASTRAX_SERVER_TAG: [],
    Config.BERNUM_SERVER_TAG: []
}

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
        password = f.request.form['password']

        user = AdminUtil.verify_admin_user(email, password)
        if user is None:
            return "Invalid Credentials"

        fl.login_user(user)
        next_page = f.request.args.get('next')
        return f.redirect(next_page) if next_page else f.redirect(
            f.url_for('main.index'))

    return f.render_template('admin/login.jinja', title='Login')


@admin_blueprint.route("/admin/logout")
@fl.login_required
def logout():
    fl.logout_user()
    return f.redirect(f.url_for('main.index'))


@admin_blueprint.route("/admin/view-external-messages")
@fl.login_required
def view_external_messages():

    filter_tag = f.request.args.get("tag", default="", type=str).strip()
    if (filter_tag != ""):
        data = Extern_Messages.query \
                .filter(Extern_Messages.tags.like(f'%#{filter_tag}$%')) \
                .order_by(Extern_Messages.timestamp.desc()).paginate(per_page=20)
    else:
        data = Extern_Messages.query \
                .order_by(Extern_Messages.timestamp.desc()).paginate(per_page=20)

    return f.render_template(
        'admin/external-messages.jinja',
        title='Extern-Messages',
        data=data
    )


def server_checkin_callback(message: Extern_Messages):
    servers = [Config.ASTRAX_SERVER_TAG, Config.BERNUM_SERVER_TAG]

    return_string = ""

    for server in servers:
        if (message.tags_contains(server)):

            data = Extern_Messages.query \
                    .filter(Extern_Messages.tags.like(f'%#{server}$%')) \
                    .filter(Extern_Messages.tags.like(f'%#{Config.SERVER_OFFLINE_TAG}$%')) \
                    .first()

            if data != None:
                # Server has come back alive and is no longer offline
                db.session.delete(data)
                db.session.commit()

            if len(server_messages_queue[server]) > 0:
                return_string = server_messages_queue[server].pop()

                timestamp = datetime.now()
                id = Util.create_uuid()
                item = Extern_Messages(
                    id = id,
                    user=Config.INTERNAL_USER,
                    message=f"{return_string}| sent",
                    timestamp=timestamp,
                    tags=Extern_Messages.create_tags([Config.INTERNAL_USER, "oplog"])
                )

                db.session.add(item)
                db.session.commit()

            break

    return return_string



@admin_blueprint.route("/admin/add-server-command", methods=['post'])
def add_server_command():
    '''
    End point for adding commands to the server_messages_queue
    '''

    '''
    Example cURL call:
        curl -X POST -F "pass=testpass" -F "op=restart -F "server=astrax"
        http://localhost:5000/admin/add-server-command
    '''
    password = f.request.form['pass']

    if Util.hash_password(password) != Config.SECRET_PASS_HASH:
        f.abort(403)

    op = f.request.form['op']
    server = f.request.form['server']
    if op is None or len(op) == 0 or server is None:
        return "Invalid call to endpoint\n"

    server_messages_queue[server].append(f"operation: {op}")
    return "Added the operation to the queue.\n"


@admin_blueprint.route("/admin/log-external-message", methods=['post'])
def log_external_message():
    '''
    End point for external messages such as local server
    logs and local server status reports.
    '''

    '''
    Example cURL call:
        curl -X POST -F "pass=testpass" -F "user=suchi"
        -F "message=asdg" -F "tags=tags"
        http://localhost:5000/admin/log-external-message
    '''
    password = f.request.form['pass']

    if Util.hash_password(password) != Config.SECRET_PASS_HASH:
        f.abort(403)

    id = Util.create_uuid()
    timestamp = datetime.now()
    user = f.request.form['user']
    message = f.request.form['message']
    tags = f.request.form['tags'].split(",")
    tags = ",".join(map(lambda item: f"#{item}$", tags))

    item = Extern_Messages(
        id = id,
        user=user,
        message=message,
        timestamp=timestamp,
        tags=tags
    )

    db.session.add(item)
    db.session.commit()


    # Callbacks must return strings.
    callbacks = {
        Config.SERVER_CHECKIN_TAG: [server_checkin_callback]
    }

    lines = []
    for tag, func_list in callbacks.items():
        if item.tags_contains(tag):
            for function in func_list:
                lines.append(function(item))

    return f"Message added with uuid: {id}"


@admin_blueprint.route("/admin/re_compute_markdowns")
@fl.login_required
def re_compute_markdowns_endpoint():
    AdminUtil.recompute_markdowns(f.current_app, db)
    return "Markdowns will be recomputed."


@admin_blueprint.route("/admin/messages")
@fl.login_required
def messages():
    data = Contact.query.order_by(Contact.date.desc()).paginate(per_page=20)
    return f.render_template(
        'admin/messages.jinja',
        title='Messages',
        data=data)


@admin_blueprint.route("/admin/blacklist")
@fl.login_required
def blacklist():
    block = f.request.args.get('type')

    if block == 'ip':
        ip = f.request.args.get('ip', '')
        has_data_flag = False
        try:
            with open(Config.IP_BLACKLIST) as fin:
                data = fin.read()
                if ip in data:
                    return f"{ip} already present in the blacklist"
                if len(data.strip()) > 0:
                    has_data_flag = True

        except FileNotFoundError:
            pass

        with open(Config.IP_BLACKLIST, 'a') as fin:
            if has_data_flag:
                fin.write("\n" + ip)
            else:
                fin.write(ip)

        return f"{ip} has been added to the blacklist"

    elif block == 'message':
        message = f.request.args.get('message', '')
        has_data_flag = False

        try:
            with open(Config.MESSAGE_BLACKLIST) as fin:
                for line in fin.readlines():
                    if (not has_data_flag) and len(line.strip()) > 0:
                        has_data_flag = True
                    if message in line:
                        return "Message already present in the blacklist"

        except FileNotFoundError:
            pass

        with open(Config.MESSAGE_BLACKLIST, 'a') as fin:
            if has_data_flag:
                fin.write("\n" + message)
            else:
                fin.write(message)

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
        return f.render_template(
            'admin/url-redirects.jinja',
            title='URL Redirects',
            urls=urls)


@admin_blueprint.route("/admin/url-redirects/delete/<id>")
@fl.login_required
def url_redirects_delete(id):
    url = URL_Redirection.query.filter_by(id=id).first()
    if not url:
        f.abort(404)

    db.session.delete(url)
    db.session.commit()
    return "URL Redirect deleted."


@admin_blueprint.route("/admin/ip-logs")
@fl.login_required
def ip_logs():
    logs = IP_Logs.query.order_by(IP_Logs.date.desc()).paginate(per_page=20)
    return f.render_template('admin/ip-logs.jinja', title='IP-logs', logs=logs)


@admin_blueprint.route("/admin/ip-logs-details/<uuid>")
@fl.login_required
def ip_log_details(uuid):
    details = IP_Logs.query.filter_by(id=uuid).first()
    return f.render_template('admin/ip-logs-details.jinja', data=details)

import flask as f
import markupsafe
import requests
import os
from cachetools import cached, TTLCache
from datetime import datetime
from ...util import Util
from ...models import URL_Redirection, Contact
from ...config import Config
from ... import db

main_blueprint = f.Blueprint("main", __name__)
contact_alert = False

# Simple in-memory cache with a TTL of 5 minutes
ics_cache = TTLCache(maxsize=1, ttl=300)


@main_blueprint.route("/session/get")
def get_session():
    return f'{f.session.get("value")}'


@main_blueprint.route("/session/set/<value>")
def set_session(value):
    f.session.permanent = True
    f.session["value"] = value
    return "Session set"


@main_blueprint.route("/")
def index():
    return f.render_template(
        "main/index.jinja", title="Home | Suchicodes", skills=Util.get_skill_list()
    )


@main_blueprint.route("/support_me")
def support_me():
    return f.render_template("main/support_me.jinja", title="Support Me | Suchicodes")


@main_blueprint.route("/about")
def about():
    return f.render_template("main/about.jinja", title="About | Suchicodes")


@main_blueprint.route("/picture-dropoff", methods=["GET", "POST"])
def picture_dropoff():
    if f.request.method == "POST":
        uploader = f.request.form["uploader"]
        uploaded_files = f.request.files.getlist("file[]")

        for file in uploaded_files:
            date = datetime.now()
            if not file.filename:
                file.filename = "nofilename"

            file.filename = f"{uploader}__{date}__{file.filename}"
            file.save(
                os.path.join(f.current_app.config["DATA_DIRECTORY"], file.filename)
            )

    return f.render_template(
        "misc/picture-dropoff.jinja", title="Upload Pictures | Suchicodes"
    )


@main_blueprint.route("/u/<keyword>")
@main_blueprint.route("/url/<keyword>")
def url_redirection(keyword):
    url = URL_Redirection.query.filter_by(keyword_in=keyword).first()
    if not url:
        f.abort(404)
        return

    return f.redirect(url.url_out)


@main_blueprint.route("/calendar")
def calendar():
    return f.render_template("main/calendar.jinja", title="Calendar | Suchicodes")


@cached(ics_cache)
def fetch_ics_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        f.abort(500, description="Failed to fetch calendar data")


@main_blueprint.route("/proxy-calendar-private")
def proxy_calendar_private():
    ics_data = fetch_ics_data(Config.PROTON_CAL_PRIVATE)
    return f.Response(ics_data, content_type="text/calendar")


@main_blueprint.route("/proxy-calendar-public")
def proxy_calendar_public():
    ics_data = fetch_ics_data(Config.PROTON_CAL_PUBLIC)
    return f.Response(ics_data, content_type="text/calendar")


@main_blueprint.route("/contact", methods=["get", "post"])
def contact():
    alert = False
    if f.request.method == "POST":
        ip = f.request.environ.get("HTTP_X_REAL_IP", f.request.remote_addr)
        if ip is None:
            ip = f.request.remote_addr
        else:
            try:
                index = ip.index(",")
                ip = ip[:index]
            except ValueError:
                pass

        sub = markupsafe.escape(f.request.form["subject"])
        message = markupsafe.escape(f.request.form["message"])
        human_test = markupsafe.escape(f.request.form["humantest"])

        if human_test.strip() != "I am human":
            return "You were classified as a bot."

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
                    if line.strip() != "" and line.strip() in message:
                        return "No"
        except FileNotFoundError:
            pass

        Util.log_contact_message(
            message=message,
            subject=sub,
            ip=ip,
            ContactModel=Contact,
            db=db,
            app=f.current_app,
        )
        alert = True

    return f.render_template(
        "main/contact.jinja", title="Contact | Suchicodes", alert=alert
    )


@main_blueprint.route("/resume.pdf")
@main_blueprint.route("/resume")
def send_pdf():
    return f.send_from_directory(f.current_app.config["RESOURCES_DIR"], "resume.pdf")


@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    if f.request.path.startswith("/api/"):
        return "Error 404, page not found. Invalid call to API.\n"

    return f.render_template("error-pages/404.jinja"), 404

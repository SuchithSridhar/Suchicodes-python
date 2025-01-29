import flask as f

well_known_blueprint = f.Blueprint("well_known", __name__)


@well_known_blueprint.route("/.well-known/")
@well_known_blueprint.route("/.well-known")
def index():
    links = [
        "robots.txt",
        "security.txt",
        "sitemap.xml",
        "pgp-key.txt",
        "humans.txt",
    ]

    return f.render_template("main/well-known.jinja", links=links)


@well_known_blueprint.route("/robots.txt")
@well_known_blueprint.route("/.well-known/robots.txt")
def robots_txt():
    data_dir = f.current_app.config["RESOURCES_DIR"]
    return f.send_from_directory(data_dir, "robots.txt")


@well_known_blueprint.route("/security.txt")
@well_known_blueprint.route("/.well-known/security.txt")
def security_txt():
    data_dir = f.current_app.config["RESOURCES_DIR"]
    return f.send_from_directory(data_dir, "security.txt")


@well_known_blueprint.route("/sitemap.xml")
@well_known_blueprint.route("/.well-known/sitemap.xml")
def sitemap_xml():
    data_dir = f.current_app.config["RESOURCES_DIR"]
    return f.send_from_directory(data_dir, "sitemap.xml")


@well_known_blueprint.route("/pgp-key.txt")
@well_known_blueprint.route("/.well-known/pgp-key.txt")
def pgp_key_txt():
    data_dir = f.current_app.config["RESOURCES_DIR"]
    return f.send_from_directory(data_dir, "pgp-key.txt")


@well_known_blueprint.route("/humans.txt")
@well_known_blueprint.route("/.well-known/humans.txt")
def humans_txt():
    data_dir = f.current_app.config["RESOURCES_DIR"]
    return f.send_from_directory(data_dir, "humans.txt")

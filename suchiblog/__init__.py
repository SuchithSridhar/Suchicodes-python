from multiprocessing.sharedctypes import Value
import flask as f
import flask_login as fl
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()
login_manager = fl.LoginManager()
login_manager.login_view = 'admin.login'

def initialize_database(db, app):
    db.create_all(app=app)

def create_app(config_class=Config):
    global LOCALE

    from .util import Util
    from .controllers.main.routes import main_blueprint
    from .controllers.projects.routes import projects_blueprint
    from .controllers.admin.routes import admin_blueprint
    from .controllers.resources.routes import resources_blueprint
    from .models import IP_Logs

    LOCALE = Util.get_locale_data()

    app = f.Flask(__name__)
    app.config.from_object(Config)


    @app.context_processor
    def locale_context():
        LOCALE = Util.get_locale_data()
        return LOCALE

    @app.before_request
    def log_ip_address():
        ip = f.request.environ.get('HTTP_X_REAL_IP', f.request.remote_addr)
        if ip is None:
            ip = f.request.remote_addr
        else:
            try:
                index = ip.index(',')
                ip = ip[:index]
            except ValueError:
                pass
        Util.log_ip_access(ip, f.request.url, db, app, IP_Logs)

    db.init_app(app)
    login_manager.init_app(app)

    initialize_database(db=db, app=app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(resources_blueprint)

    return app

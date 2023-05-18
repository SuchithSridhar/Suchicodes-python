import flask as f
import flask_login as fl
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .logging_formatter import get_logger

db = SQLAlchemy()
login_manager = fl.LoginManager()
login_manager.login_view = 'admin.login'
migrate = Migrate()
logger = get_logger()


def initialize_database(db, app):
    with app.app_context():
        db.create_all()


def create_app(config_class=Config):
    global LOCALE

    from .util import Util
    from .controllers.main.routes import main_blueprint
    from .controllers.projects.routes import projects_blueprint
    from .controllers.admin.routes import admin_blueprint
    from .controllers.resources.routes import resources_blueprint
    from .controllers.api.routes import api_blueprint
    from .models import IP_Logs
    from .commands.scheduled_tasks import cli_blueprint

    GLOBAL_DATA = Util.get_pre_render_data(flask=None, lang='en')

    app = f.Flask(__name__)
    app.config.from_object(Config)

    @app.context_processor
    def pre_render():
        GLOBAL_DATA = Util.get_pre_render_data(flask=f, lang='en')
        return GLOBAL_DATA

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

        other_information = f.request.environ

        Util.log_ip_access(
            ip,
            other_information,
            f.request.url,
            db,
            app,
            IP_Logs)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(resources_blueprint)
    app.register_blueprint(cli_blueprint)
    app.register_blueprint(api_blueprint)

    return app

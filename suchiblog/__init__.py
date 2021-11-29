import flask as f
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def initialize_database(db, app):
    db.create_all(app=app)

def create_app(config_class=Config):
    global LOCALE

    from .util import Util
    from .controllers.main.routes import main_blueprint
    from .controllers.projects.routes import projects_blueprint

    LOCALE = Util.get_locale_data()

    app = f.Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True

    @app.context_processor
    def locale_context():
        LOCALE = Util.get_locale_data()
        return LOCALE

    db.init_app(app)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(projects_blueprint)

    return app
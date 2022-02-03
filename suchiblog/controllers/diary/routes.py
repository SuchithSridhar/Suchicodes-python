import flask as f
import flask_login as fl

diary_blueprint = f.Blueprint('diary', __name__)


@diary_blueprint.route("/sde", methods=['get'])
@diary_blueprint.route("/sde/", methods=['get'])
@fl.login_required
def index():
    return f.render_template('diary/index.jinja')

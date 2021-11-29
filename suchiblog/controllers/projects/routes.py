import flask as f
from ...models import Projects
from ...util import Util

projects_blueprint = f.Blueprint('projects', __name__)

@projects_blueprint.route("/projects")
@projects_blueprint.route("/projects/")
def index():
    try:
        data = []
        for project in Projects.query.all():
            new = {}
            new['url'] = project.url
            new['title'] = project.title
            new['brief'] = project.brief
            new['img'] = project.img
            data.append(new)
    
    except Exception:
        data = [{"title": "Some error in database"}]

    return f.render_template("projects/projects.jinja", title="Projects | Suchicodes", projects=data)

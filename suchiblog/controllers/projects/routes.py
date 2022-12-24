import os
import flask as f
import flask_login as fl
from ... import db
from ...models import Projects
from .projects_util import ProjectUtil

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

    return f.render_template(
        "projects/projects.jinja",
        title="Projects | Suchicodes",
        projects=data)


@projects_blueprint.route("/projects/<project_name>")
def project(project_name):
    project = Projects.query.filter_by(url='/projects/' + project_name).first()
    if not project:
        f.abort(404)
        return

    return f.render_template(
        'projects/single.jinja',
        title=f"{project.title} | Suchicodes",
        project_html=project.html)


@projects_blueprint.route("/admin/create_project", methods=['get', 'post'])
@fl.login_required
def create():
    if f.request.method == 'POST':
        uploaded_files = f.request.files.getlist("file[]")
        title = f.request.form['title']
        uuids = f.request.form['uuids'].split(',')
        for file in uploaded_files:
            if not file.filename:
                continue
            uuid = [x for x in uuids if file.filename in x][0].split('###')[1]
            file.save(
                os.path.join(f.current_app.config['PROJECTS_UPLOAD_FOLDER'],
                             uuid + f"{os.path.splitext(file.filename)[1]}")
            )
        url = '/projects/' + f.request.form['url']
        brief = f.request.form['brief']
        img = str(f.request.form.get('img'))
        md = f.request.form['markdown']
        html = ProjectUtil.to_html(md)
        item = Projects(
            title=title,
            url=url,
            brief=brief,
            img=img,
            markdown=md,
            html=html)
        db.session.add(item)
        db.session.commit()

    return f.render_template(
        'projects/create.jinja',
        title="Create project",
        images=ProjectUtil.get_images())


@projects_blueprint.route("/admin/edit_project/<uuid>",
                          methods=['get', 'post'])
@fl.login_required
def edit(uuid):
    project = Projects.query.filter_by(id=uuid).first()
    if not project:
        f.abort(404)
        return

    if f.request.method == 'POST':
        uploaded_files = f.request.files.getlist("file[]")
        title = f.request.form['title']
        uuids = f.request.form['uuids'].split(',')
        for file in uploaded_files:
            if not file.filename:
                continue
            file_uuid = [
                x for x in uuids if file.filename in x
            ][0].split('###')[1]
            file.save(
                os.path.join(
                    f.current_app.config['PROJECTS_UPLOAD_FOLDER'],
                    file_uuid +
                    f"{os.path.splitext(file.filename)[1]}"))
        url = '/projects/' + f.request.form['url']
        brief = f.request.form['brief']
        img = str(f.request.form.get('img'))
        md = f.request.form['markdown']
        html = ProjectUtil.to_html(md)

        project.title = title
        project.url = url
        project.brief = brief
        if img in ProjectUtil.get_images():
            project.img = img
        project.markdown = md
        project.html = html

        db.session.commit()

    return f.render_template(
        'projects/create.jinja',
        title="Create project",
        images=ProjectUtil.get_images(),
        project=project)


@projects_blueprint.route("/admin/projects")
@projects_blueprint.route("/admin/projects/")
@fl.login_required
def admin_index():
    try:
        data = []
        for project in Projects.query.all():
            new = {}
            new['id'] = project.id
            new['url'] = project.url
            new['title'] = project.title
            new['brief'] = project.brief
            new['img'] = project.img
            data.append(new)

    except Exception:
        data = [{"title": "Some error in database"}]

    return f.render_template(
        "projects/projects.jinja",
        title="Projects | Suchicodes",
        projects=data,
        admin=True)

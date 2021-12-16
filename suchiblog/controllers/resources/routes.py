import json
import os
import flask as f
import flask_login as fl
from datetime import datetime
from ... import db
from ...models import Category, Blog
from ...util import Util
from .res_util import ResUtil

resources_blueprint = f.Blueprint('resources', __name__)

@resources_blueprint.route("/resources")
@resources_blueprint.route("/resources/")
def index():
    categories = Category.query.all()
    blogs = Blog.query.all()
    categories_json = []
    for item in categories:
        new = {
            "id": item.id,
            "parent": item.parent_id,
            "category": item.category,
            "uuid": item.uuid
        }
        categories_json.append(new)

    blogs_json = []
    for item in blogs:
        new = {
            "id": item.id,
            "title": item.title,
            "brief": item.brief,
            "category": item.category
        }
        blogs_json.append(new)

    return f.render_template(
        "resources/index.jinja", title="Resources | Suchicodes",
        categories=json.dumps(categories_json), blogs=json.dumps(blogs_json)
    )


@resources_blueprint.route("/resources/blog/<uuid>")
@fl.login_required
def view_blog(uuid):
    blog = Blog.query.filter_by(id=uuid).first()
    if not blog:
        f.abort(404)
        return

    return f.render_template('resources/blog.jinja', title=f"{blog.title} | Suchicodes", blog_html=blog.html)


@resources_blueprint.route("/admin/create_blog", methods=['get','post'])
@fl.login_required
def create_blog():
    if f.request.method == 'POST':
        uploaded_files = f.request.files.getlist("file[]")
        uuids = f.request.form['uuids'].split(',')
        for file in uploaded_files:
            if not file.filename:
                continue
            uuid = [x for x in uuids if file.filename in x][0].split('###')[1]
            file.save(
                os.path.join(f.current_app.config['PROJECTS_UPLOAD_FOLDER'],
                uuid+f"{os.path.splitext(file.filename)[1]}")
            )
        title = f.request.form['title']
        brief = f.request.form['brief']
        date = datetime.now()
        category = (f.request.form.get('category'))
        md = f.request.form['markdown']
        html = ResUtil.to_html(md)
        item = Blog(title=title, date=date, brief=brief, category=category, markdown=md, html=html)
        db.session.add(item)
        db.session.commit()

    return f.render_template('resources/create.jinja', title="Create Blog", categories=ResUtil.get_categories())

@resources_blueprint.route("/admin/edit_blog/<uuid>",  methods=['get', 'post'])
@fl.login_required
def edit(uuid):
    blog = Blog.query.filter_by(id=uuid).first()
    if not blog:
        f.abort(404)
        return

    if f.request.method == 'POST':
        uploaded_files = f.request.files.getlist("file[]")
        uuids = f.request.form['uuids'].split(',')
        for file in uploaded_files:
            if not file.filename:
                continue
            file_uuid = [x for x in uuids if file.filename in x][0].split('###')[1]
            file.save(
                os.path.join(f.current_app.config['PROJECTS_UPLOAD_FOLDER'],
                file_uuid+f"{os.path.splitext(file.filename)[1]}")
            )
        title = f.request.form['title']
        brief = f.request.form['brief']
        category = (f.request.form.get('category'))
        md = f.request.form['markdown']
        html = ResUtil.to_html(md)

        blog.title=title
        blog.brief=brief
        if category in ResUtil.get_categories().values():
            blog.category=category
        blog.markdown=md
        blog.html=html

        db.session.commit()

    return f.render_template('resources/create.jinja', title="Edit Blog", categories=ResUtil.get_categories(), blog=blog)


@resources_blueprint.route("/admin/create_category", methods=['get','post'])
@fl.login_required
def create_category():
    if f.request.method == 'POST':
        id = f.request.form['id']
        title = f.request.form['title']
        parent = int(f.request.form.get('category'))
        uuid = Util.create_uuid[0:6]
        item = Category(id=int(id), parent_id=parent, category=title, uuid=uuid)
        db.session.add(item)
        db.session.commit()

    return f.render_template('resources/create-category.jinja', title="Create Category", categories=ResUtil.get_categories())



@resources_blueprint.route("/admin/edit_category/<id>", methods=['get','post'])
@fl.login_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first()
    if not category:
        f.abort(404)
        return

    if f.request.method == 'POST':
        id = f.request.form['id']
        title = f.request.form['title']
        try:
            parent = int(f.request.form.get('category'))
        except ValueError:
            parent = 0

        category.category=title
        category.id=int(id)
        category.parent_id=parent

        db.session.commit()

    return f.render_template('resources/create-category.jinja', title="Edit Category", categories=ResUtil.get_categories(), category=category)



@resources_blueprint.route("/admin/view_categories")
@fl.login_required
def view_category():
    categories = Category.query.all()
    return f.render_template('resources/view-categories.jinja', title="View Category", categories=categories)

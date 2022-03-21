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


@resources_blueprint.route("/resources/blog/<selector>")
def view_blog(selector):
    blog = Blog.query.filter_by(id=selector).first()
    if not blog:
        for b in Blog.query.all():
            if b.title.lower().replace(' ', '-').replace("'", '') == selector.lower():
                blog = b
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
        md = f.request.form['markdown']
        md_edited = md
        for file in uploaded_files:
            if not file.filename:
                continue
            uuid = [x for x in uuids if file.filename in x][0].split('###')[1]
            new_file_name = uuid+f"{os.path.splitext(file.filename)[1]}"
            file.save(
                os.path.join(f.current_app.config['PROJECTS_UPLOAD_FOLDER'],
                new_file_name
                )
            )

            start = md_edited.find(file.filename)
            open_brace = ResUtil.find_open_brace(md_edited, start)
            close_brace = md_edited.find(")", start)
            md_edited = md_edited[:open_brace+1] + new_file_name + md_edited[close_brace:]

        title = f.request.form['title']
        brief = f.request.form['brief']
        date = datetime.now()
        category = (f.request.form.get('category'))
        html = ResUtil.to_html(md_edited)
        item = Blog(title=title, date=date, brief=brief,
                category=category, markdown=md_edited, html=html)
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
        md = f.request.form['markdown']
        md_edited = md
        for file in uploaded_files:
            if not file.filename:
                continue
            file_uuid = [x for x in uuids if file.filename in x][0].split('###')[1]
            new_file_name = uuid+f"{os.path.splitext(file.filename)[1]}"
            file.save(
                os.path.join(f.current_app.config['PROJECTS_UPLOAD_FOLDER'],
                new_file_name
                )
            )

            start = md_edited.find(file.filename)
            open_brace = ResUtil.find_open_brace(md_edited, start)
            close_brace = md_edited.find(")", start)
            md_edited = md_edited[:open_brace+1] + new_file_name + md_edited[close_brace:]

        title = f.request.form['title']
        brief = f.request.form['brief']
        category = (f.request.form.get('category'))
        html = ResUtil.to_html(md)

        blog.title=title
        blog.brief=brief
        if category in ResUtil.get_categories().values():
            blog.category=category
        blog.markdown=md_edited
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
        uuid = Util.create_uuid()[0:6]
        item = Category(id=int(id), parent_id=parent, category=title, uuid=uuid)
        db.session.add(item)
        db.session.commit()

    return f.render_template('resources/create-category.jinja', title="Create Category", categories=ResUtil.get_categories_with_id())



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

    return f.render_template('resources/create-category.jinja', title="Edit Category", categories=ResUtil.get_categories_with_id(), category=category)



@resources_blueprint.route("/admin/view_categories")
@fl.login_required
def view_category():
    categories = Category.query.all()
    return f.render_template('resources/view-categories.jinja', title="View Category", categories=categories)

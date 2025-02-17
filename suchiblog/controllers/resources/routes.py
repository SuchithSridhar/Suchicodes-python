import json
import os
from datetime import datetime
import flask as f
import flask_login as fl
from ... import db
from ...models import Category, Blog
from ...util import Util
from .res_util import ResUtil

resources_blueprint = f.Blueprint("resources", __name__)


@resources_blueprint.route("/resources/")
def index():
    return f.render_template("resources/index.jinja", title="Resources | Suchicodes")


@resources_blueprint.route("/resources/categories/")
def get_categories():
    categories = Category.query.all()
    blogs = Blog.query.all()
    categories_json = []
    for item in categories:
        if item.parent_id is None:
            parent_id = 0
        else:
            parent_id = item.parent_id

        new = {"id": item.id, "parent": parent_id, "name": item.name, "uuid": item.uuid}
        categories_json.append(new)

    blogs_json = []
    for item in blogs:
        new = {
            "id": item.id,
            "title": item.title,
            "brief": item.brief,
            "category": item.category_id,
        }
        blogs_json.append(new)

    return f.render_template(
        "resources/all-categories.jinja",
        title="Resources - Categories | Suchicodes",
        categories=json.dumps(categories_json),
        blogs=json.dumps(blogs_json),
    )


@resources_blueprint.route("/resources/search")
def search_blogs():
    # Number of results to return
    item_count = 10

    search_query = f.request.args.get("query", default="", type=str).strip()
    results = []
    if search_query != "":
        cut_off = 50  # cut off for match result
        fuzz_search = ResUtil.perform_fuzzy_search(search_query, item_count)
        fuzz_search = reversed(sorted(fuzz_search, key=lambda k: k["ratio"]))
        for result in fuzz_search:
            if result["ratio"] < cut_off:
                break
            path = (x[1] for x in ResUtil.get_category_path(result["category"]))
            path = " > ".join(path)
            results.append(
                {
                    "blog_id": result["blog_id"][:6],
                    "blog_title": result["blog_title"],
                    "blog_path": path,
                    "matched_line": result["line"],
                }
            )

    return f.render_template(
        "resources/search.jinja", title="Search Blogs | Suchicodes", results=results
    )


@resources_blueprint.route("/resources/blog/<selector>")
def view_blog(selector):
    blog = Blog.query.filter_by(id=selector).first()
    if not blog:
        for b in Blog.query.all():
            search_query = b.title.lower().replace(" ", "-").replace("'", "")
            if search_query == selector.lower():
                blog = b
                break

            if b.id[0 : len(selector)] == selector:
                blog = b
                break

    if not blog:
        f.abort(404)

    return f.render_template(
        "resources/blog.jinja",
        title=f"{blog.title} | Suchicodes",
        blog_html=blog.html,
        admin=fl.current_user.is_authenticated,
        blog=blog,
    )


@resources_blueprint.route("/admin/create_blog", methods=["get", "post"])
@fl.login_required
def create_blog():
    if f.request.method == "POST":
        uploaded_files = f.request.files.getlist("file[]")
        uuids = f.request.form["uuids"].split(",")
        md = f.request.form["markdown"]
        md_edited = md
        picture_map = {}

        for file in uploaded_files:
            if not file.filename:
                continue
            uuid = [x for x in uuids if file.filename in x][0].split("###")[1]
            new_file_name = uuid + f"{os.path.splitext(file.filename)[1]}"
            file.save(
                os.path.join(
                    f.current_app.config["PROJECTS_UPLOAD_FOLDER"], new_file_name
                )
            )

            picture_map[file.filename] = uuid
            start = md_edited.find(file.filename)
            open_brace = ResUtil.find_open_parenthesis(md_edited, start)
            close_brace = md_edited.find(")", start)
            md_edited = (
                md_edited[: open_brace + 1] + new_file_name + md_edited[close_brace:]
            )

        title = f.request.form["title"]
        brief = f.request.form["brief"]
        date = datetime.now()
        category = f.request.form.get("category")

        if category is not None:
            if category == "":
                category = None

            else:
                category = int(category)

        html = ResUtil.to_html(md_edited)
        item = Blog(
            title=title,
            date_created=date,
            date_updated=date,
            brief=brief,
            category_id=category,
            markdown=md_edited,
            html=html,
            picture_map=json.dumps(picture_map),
        )
        db.session.add(item)
        db.session.commit()

    return f.render_template(
        "resources/create.jinja",
        title="Create Blog",
        categories=ResUtil.get_categories_ids(),
    )


@resources_blueprint.route("/admin/edit_blog/<uuid>", methods=["get", "post"])
@fl.login_required
def edit(uuid):
    blog = Blog.query.filter_by(id=uuid).first()
    if not blog:
        f.abort(404)

    picture_map = json.loads(blog.picture_map)
    if f.request.method == "POST":
        uploaded_files = f.request.files.getlist("file[]")
        uuids = f.request.form["uuids"].split(",")
        md = f.request.form["markdown"]
        md_edited = md
        for file in uploaded_files:
            if not file.filename:
                continue
            file_uuid = [x for x in uuids if file.filename in x][0].split("###")[1]
            new_file_name = file_uuid + f"{os.path.splitext(file.filename)[1]}"
            file.save(
                os.path.join(
                    f.current_app.config["PROJECTS_UPLOAD_FOLDER"], new_file_name
                )
            )

            picture_map[file.filename] = uuid
            start = md_edited.find(file.filename)
            open_brace = ResUtil.find_open_parenthesis(md_edited, start)
            close_brace = md_edited.find(")", start)
            md_edited = (
                md_edited[: open_brace + 1] + new_file_name + md_edited[close_brace:]
            )

        title = f.request.form["title"]
        brief = f.request.form["brief"]
        category = f.request.form.get("category")
        html = ResUtil.to_html(md_edited)

        blog.title = title
        blog.brief = brief

        if category is not None:
            if category == "":
                category = None

            else:
                category = int(category)

        if category in list(ResUtil.get_categories_ids().values()):
            blog.category_id = category

        blog.markdown = md_edited
        blog.html = html
        blog.picture_map = json.dumps(picture_map)
        blog.date_updated = datetime.now()

        db.session.commit()

    return f.render_template(
        "resources/create.jinja",
        title="Edit Blog",
        categories=ResUtil.get_categories_ids(),
        blog=blog,
    )


@resources_blueprint.route("/admin/create_category", methods=["get", "post"])
@fl.login_required
def create_category():
    if f.request.method == "POST":
        id = f.request.form["id"]
        title = f.request.form["title"]
        parent = f.request.form.get("category")

        # If $parent is none, it's a top level category
        if parent is not None:
            if parent == "":
                parent = None

            else:
                parent = int(parent)

        uuid = Util.create_uuid()[0:6]
        item = Category(id=int(id), parent_id=parent, name=title, uuid=uuid)
        db.session.add(item)
        db.session.commit()

    return f.render_template(
        "resources/create-category.jinja",
        title="Create Category",
        categories=ResUtil.get_categories_ids(),
    )


@resources_blueprint.route("/admin/edit_category/<id>", methods=["get", "post"])
@fl.login_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first()
    if not category:
        f.abort(404)
        return

    if f.request.method == "POST":
        id = f.request.form["id"]
        title = f.request.form["title"]
        parent = f.request.form.get("category")

        # If $parent is none, it's a top level category
        if parent is not None:
            if parent == "":
                parent = None

            else:
                parent = int(parent)

        category.name = title
        category.id = int(id)
        category.parent_id = parent

        db.session.commit()

    return f.render_template(
        "resources/create-category.jinja",
        title="Edit Category",
        categories=ResUtil.get_categories_ids(),
        category=category,
    )


@resources_blueprint.route("/admin/view_categories")
@fl.login_required
def view_category():
    categories = Category.query.all()
    return f.render_template(
        "resources/view-categories.jinja", title="View Category", categories=categories
    )

import json
import flask as f
from datetime import datetime
from flask import jsonify
from ...models import Category, Blog
from ..admin.admin_util import AdminUtil
from .api_util import ApiUtil
from ..resources.res_util import ResUtil
from ...config import Config
from ... import db

api_blueprint = f.Blueprint('api', __name__)


@api_blueprint.route("/api/")
def api_help():
    '''Help information about API.'''

    return f.render_template(
        'api/help.jinja',
        title="Api Help | Suchicodes"
        )


@api_blueprint.route("/api/resources/categories")
def get_categories():
    '''Get all categories defined under resources.'''

    categories = Category.query.all()
    response = []
    for cat in categories:
        if cat.name == "deleted":
            continue

        response.append({
            "id": cat.id,
            "parent_id": cat.parent_id,
            "name": cat.name,
        })

    return jsonify(response)


@api_blueprint.route("/api/resources/blogs/<category_id>")
def get_blogs_in_category(category_id):
    '''Api endpoint to get all blogs in a given category using its ID.'''

    category = Category.query.filter_by(id=int(category_id)).first()
    if category.name == "deleted":
        return jsonify([])

    blogs = Blog.query.all()
    response = []
    for blog in blogs:

        if blog.category_id != category.id:
            continue

        response.append({
            "id": blog.id,
            "date": blog.date,
            "title": blog.title,
            "brief": blog.brief,
            "markdown_length": len(blog.markdown)
        })

    return jsonify(response)


@api_blueprint.route("/api/resources/blog/<blog_id>")
def get_blog_content(blog_id):
    '''Get the data of a blog using its ID.'''

    blog = Blog.query.filter_by(id=blog_id).first()
    blog_category = Category.query.filter_by(id=blog.category_id).first()

    if blog_category.name == "deleted":
        return jsonify({})

    blog_data = {
                "id": blog.id,
                "date": blog.date,
                "title": blog.title,
                "brief": blog.brief,
                "markdown": blog.markdown,
                "html": blog.html,
                "category": blog_category.name
    }

    return jsonify(blog_data)


@api_blueprint.route("/api/admin/upload_blog", methods=['post'])
def upload_blog():
    email = f.request.form.get('email', '')
    password = f.request.form.get('password', '')
    user = AdminUtil.verify_admin_user(email, password)

    if user is None:
        return "Credentials invalid.\n"

    uploaded_files = dict(f.request.files.lists()).get("files[]", [])
    files = ApiUtil.categorize_files(uploaded_files)

    if files['config'] is None:
        return "Config file not included in files."\
               f" Please include a '{Config.NOTES_CONFIG_FILENAME}'"\
               " in the list of files uploaded.\n"

    config = json.load(files['config'])
    verified, missing_field = ApiUtil.verify_blog_config(config)

    if not verified:
        return f"Config was missing field: {missing_field}\n"

    if files['markdown'] is None:
        return "Markdown file missing from upload.\n"

    markdown = files['markdown'].read().decode("UTF-8")

    # Check if blog is being updated
    if config.get(ApiUtil.BLOG_ID, None) is not None:
        blog = Blog.query.filter_by(id=config.get(ApiUtil.BLOG_ID)).first()
        if blog is None:
            return "Blog with blog_id not found\n"

        picture_map = json.loads(blog.picture_map)
    else:
        blog = None
        picture_map = {}

    # Save the required files
    picture_map = ApiUtil.save_required_files(
        files['pictures'],
        picture_map
    )

    # Generate all the data
    markdown = ApiUtil.substitute_picute_paths(markdown, picture_map)
    html = ResUtil.to_html(markdown)
    markdown = markdown
    brief = config[ApiUtil.BLOG_BRIEF]
    title = config[ApiUtil.BLOG_TITLE]
    category_id = int(config[ApiUtil.BLOG_CATEGORY])
    picture_map_str = json.dumps(picture_map)
    date = datetime.now()

    # Update existing blog
    if blog is not None:
        status = "Updated existing blog"
        blog.html = html
        blog.markdown = markdown
        blog.brief = brief
        blog.title = title
        blog.category_id = category_id
        blog.picture_map = picture_map_str
        blog.date_updated = date

    # Create new blog
    else:
        status = "Created new blog"
        blog = Blog(
            html=html,
            markdown=markdown,
            brief=brief,
            title=title,
            category_id=category_id,
            picture_map=picture_map_str,
            date_updated=date,
            date_created=date
        )
        db.session.add(blog)
    db.session.commit()

    return_data = {
        "id": blog.id,
        "status": status
    }

    return jsonify(return_data)

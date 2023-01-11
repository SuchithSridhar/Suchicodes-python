import flask as f
from flask import jsonify
from ...models import Category, Blog

api_blueprint = f.Blueprint('api', __name__)


@api_blueprint.route("/api/resources/categories")
def get_categories():
    '''Get all categories defined under resources.'''

    categories = Category.query.all()
    response = []
    for cat in categories:
        if cat.category != "deleted":
            response.append({
                "id": cat.id,
                "parent_id": cat.parent_id,
                "name": cat.category,
            })
    return jsonify(response)


@api_blueprint.route("/api/resources/blogs/<category_id>")
def get_blogs_in_category(category_id):
    '''Api endpoint to get all blogs in a given category using its ID.'''

    category = Category.query.filter_by(id=int(category_id)).first()
    if category.category.lower() == "deleted":
        return jsonify([])

    blogs = Blog.query.all()
    response = []
    for blog in blogs:
        if blog.category == category.uuid:
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
    blog_category = Category.query.filter_by(uuid=blog.category).first()
    if blog_category.category.lower() == "deleted":
        return jsonify({})

    blog_data = {
                "id": blog.id,
                "date": blog.date,
                "title": blog.title,
                "brief": blog.brief,
                "markdown": blog.markdown,
                "html": blog.html,
                "category": blog_category.category
    }
    return jsonify(blog_data)


@api_blueprint.route("/api/")
def api_help():
    '''Help information about API.'''

    return f.render_template(
        'api/help.jinja',
        title="Api Help | Suchicodes"
        )

import flask as f
from ...models import URL_Redirection
from ...config import Config
from ... import db
from ...models import Category, Blog
from flask import jsonify

api_blueprint = f.Blueprint('api', __name__)

@api_blueprint.route("/api/resources/categories")
def get_categories():
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
    category = Category.query.filter_by(id=int(category_id)).first()
    if category.category == "deleted":
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
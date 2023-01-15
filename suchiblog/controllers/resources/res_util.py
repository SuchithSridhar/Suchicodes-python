from rapidfuzz import fuzz
import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from ...models import Category
from ...models import Blog
from ...config import Config


class ResUtil:
    def get_category_path(category_uuid: str):
        tree = []
        category = Category.query.filter_by(uuid=category_uuid).first()
        while (category.parent_id != 0):
            tree = [(category.uuid, category.category)] + tree
            category = Category.query.filter_by(id=category.parent_id).first()

        tree = [(category.uuid, category.category)] + tree
        return tree

    def perform_fuzzy_search(query: str, count: int, category_id: str = None):
        all_blogs = Blog.query.all()
        deleted_category_uuid = Category.query.filter_by(id=Config.DELETED_CATEGORY_ID).first().uuid
        results = []
        top_ratios = []
        for blog in all_blogs:
            if blog.category == deleted_category_uuid:
                continue

            if category_id is not None and category_id != blog.category:
                continue

            for index, line in enumerate(blog.markdown.split("\n")):
                ratio = fuzz.token_set_ratio(line, query)

                if len(top_ratios) < count:
                    result_item = {
                        "index": index,
                        "blog_id": blog.id,
                        "ratio": ratio,
                        "line": line,
                        "blog_title": blog.title,
                        "category": blog.category
                    }
                    results.append(result_item)
                    top_ratios.append(ratio)

                elif min(top_ratios) < ratio:
                    result_item = {
                        "index": index,
                        "blog_id": blog.id,
                        "ratio": ratio,
                        "line": line,
                        "blog_title": blog.title,
                        "category": blog.category
                    }
                    index = top_ratios.index(min(top_ratios))
                    top_ratios[index] = ratio
                    results[index] = result_item

        return results

    def get_categories():
        cats = Category.query.all()
        cats_dict = {x.category: x.uuid for x in cats}
        return cats_dict

    def get_categories_with_id():
        cats = Category.query.all()
        cats_dict = {x.category: x.id for x in cats}
        return cats_dict

    def to_html(md):
        md = md.replace('\r\n', '\n') + "\n\n\n[TOC]"
        html = markdown.markdown(
            md,
            extensions=[
                TocExtension(),
                CodeHiliteExtension(
                    guess_lang=False),
                FencedCodeExtension()])
        return html

    def find_open_brace(md, start):
        if md[start] == "(":
            return start
        else:
            return ResUtil.find_open_brace(md, start - 1)

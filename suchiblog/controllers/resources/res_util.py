from rapidfuzz import fuzz
import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from ...models import Category
from ...models import Blog
from ...config import Config


class ResUtil:
    @staticmethod
    def get_category_path(category_id: int):
        tree = []
        category = Category.query.filter_by(id=category_id).first()
        while (category is not None and category.parent_id is not None):
            tree = [(category.id, category.name)] + tree
            category = Category.query.filter_by(id=category.parent_id).first()

        tree = [(category.id, category.name)] + tree
        return tree

    @staticmethod
    def perform_fuzzy_search(query: str, count: int, category_id: str = ''):
        all_blogs = Blog.query.all()
        results = []
        top_ratios = []
        for blog in all_blogs:
            if blog.category_id == Config.DELETED_CATEGORY_ID:
                continue

            if category_id != '' and category_id != blog.category_id:
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
                        "category": blog.category_id
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
                        "category": blog.category_id
                    }
                    index = top_ratios.index(min(top_ratios))
                    top_ratios[index] = ratio
                    results[index] = result_item

        return results

    @staticmethod
    def get_categories_uuids():
        cats = Category.query.all()
        cats_dict = {x.name: x.uuid for x in cats}
        return cats_dict

    @staticmethod
    def get_categories_ids():
        cats = Category.query.all()
        cats_dict = {x.name: x.id for x in cats}
        return cats_dict

    @staticmethod
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

    @staticmethod
    def find_open_parenthesis(md, start):
        index = start
        while (md[index] != "("):
            index -= 1
        return index

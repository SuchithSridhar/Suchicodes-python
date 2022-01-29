import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from numpy import False_
from ...models import Category, Blog
from ...util import Util

class ResUtil:
    def get_categories():
        cats = Category.query.all()
        cats_dict = { x.category : x.uuid for x in cats }
        return cats_dict

    def get_categories_with_id():
        cats = Category.query.all()
        cats_dict = { x.category : x.id for x in cats }
        return cats_dict

    def create_categories(db):
        cats = []
        Category.query.delete()
        cats.append(Category(id=10_000, parent_id=0,      uuid="8a393e", category="Linux Desktop"))
        cats.append(Category(id=20_000, parent_id=0,      uuid="5c2738", category="Server Admin"))

        cats.append(Category(id=30_000, parent_id=0,      uuid="68947a", category="Programming"))
        cats.append(Category(id=31_000, parent_id=30_000, uuid="107fc0", category="Python"))
        cats.append(Category(id=32_000, parent_id=30_000, uuid="5a84ea", category="Javascript"))
        cats.append(Category(id=33_000, parent_id=30_000, uuid="cbb215", category="Java"))
        cats.append(Category(id=34_000, parent_id=30_000, uuid="6e8a99", category="Ruby"))
        cats.append(Category(id=35_000, parent_id=30_000, uuid="5534d2", category="Bash"))

        cats.append(Category(id=40_000, parent_id=0,      uuid="3da74e", category="Science"))
        cats.append(Category(id=41_000, parent_id=40_000, uuid="a66c9f", category="Biology"))
        cats.append(Category(id=42_000, parent_id=40_000, uuid="ebb82b", category="Chemistry"))
        cats.append(Category(id=43_000, parent_id=40_000, uuid="eb86fd", category="Physics"))

        cats.append(Category(id=50_000, parent_id=0,      uuid="b1e355", category="Philosophy"))
        cats.append(Category(id=51_000, parent_id=50_000, uuid="801b2a", category="Atheism"))
        cats.append(Category(id=60_000, parent_id=0,      uuid="10bf9a", category="UNB Lectures"))
        cats.append(Category(id=60_100, parent_id=60_000, uuid="0a5d57", category="CS-1073"))
        cats.append(Category(id=60_200, parent_id=60_000, uuid="6c87be", category="CS-1083"))
        cats.append(Category(id=60_300, parent_id=60_000, uuid="b28a98", category="CS-1203"))

        cats.append(Category(id=70_000, parent_id=0,      uuid="401a1e", category="Misc"))
        cats.append(Category(id=999_999, parent_id=0,     uuid="d4c232", category="deleted"))

        for item in cats:
            db.session.add(item)

        db.session.commit()
    
    def to_html(md):
        md = md.replace('\r\n', '\n') + "\n\n\n[TOC]"
        html = markdown.markdown(md, extensions=[TocExtension(), CodeHiliteExtension(guess_lang=False), FencedCodeExtension()])
        return html

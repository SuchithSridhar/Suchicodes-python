from multiprocessing import Process
from ...models import Blog
from ...controllers.resources.res_util import ResUtil

def re_compute_markdowns(app, db):
    proc = Process(target=re_compute, args=(app, db))
    proc.start()
    proc.join()


def re_compute(app, db):
    with app.app_context():
        blogs = Blog.query.all()
        for blog in blogs:
            blog.html = ResUtil.to_html(blog.markdown)
        db.session.commit()


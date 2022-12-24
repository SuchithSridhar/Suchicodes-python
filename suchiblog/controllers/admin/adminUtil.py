from multiprocessing import Process
from ...models import Blog
from ...controllers.resources.res_util import ResUtil
import threading
import datetime
import os


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


def server_checkin(status: str, file: str):
    threading.Thread(
        target=server_checkin_background,
        name="server-checkin",
        args=[
            status,
            file]).start()


def server_checkin_background(status: str, file: str):
    mode = 'w'
    new_line = ""

    if (os.path.isfile(file)):
        mode = 'a'
        new_line = "\n"

    status = status.replace(",", "<comma>")
    date = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
    new_line += f"{date},{status}"

    with open(file, mode) as f:
        f.write(new_line)

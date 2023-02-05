from ...models import Blog, Admin
from ...controllers.resources.res_util import ResUtil
from ...config import Config
from ...util import Util
import threading
import datetime
import os


class AdminUtil:

    @staticmethod
    def verify_admin_user(email: str, password: str):
        '''Get the user based on email and password.
        Returns None if user is not found.'''

        password_hash = Util.hash_password(password)
        user = Admin.query.filter_by(email=email).first()

        if user is None:
            return user

        decoded = user.password.decode('UTF-8')

        if (decoded == password_hash or
            user.password == password_hash or
                user.password == password):
            return user

        return None

    @staticmethod
    def run_background(func, name: str, args: list):
        '''Run $func function in the background and give it
        a name $name and $args are passed to $func.
        '''

        threading.Thread(
            target=func,
            name=name,
            args=args
        ).start()

    @staticmethod
    def recompute_markdowns(app, db):
        def func(app, db):
            with app.app_context():
                blogs = Blog.query.all()
                for blog in blogs:
                    blog.html = ResUtil.to_html(blog.markdown)
                db.session.commit()

        AdminUtil.run_background(func, 'recompute-markdowns', args=[app, db])

    @staticmethod
    def server_checkin(status: str, file: str):
        def func(status: str, file: str):
            mode = 'w'
            new_line = ""

            if (Config.SUCHI_SERVER_VAIDATION is None):
                # TODO: Log this as an ERROR
                return

            if (os.path.isfile(Config.SUCHI_SERVER_VAIDATION)):
                os.remove(Config.SUCHI_SERVER_VAIDATION)

            if (os.path.isfile(file)):
                mode = 'a'
                new_line = "\n"

            status = status.replace(",", "<comma>")
            date = datetime.datetime.now()
            date_str = date.strftime(Config.DATETIME_COMPLETE_FORMAT)
            new_line += f"{date_str},{status}"

            with open(file, mode) as f:
                f.write(new_line)

        AdminUtil.run_background(
            func,
            "server-checkin",
            args=[status, file]
        )

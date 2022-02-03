import flask as f
import flask_login as fl
from ...models import User
from ...util import Util
from ...config import Config
from ... import db

users_blueprint = f.Blueprint('users', __name__)


@users_blueprint.route("/login", methods=['get', 'post'])
def login():
    if fl.current_user.is_authenticated:
        return f.redirect(f.url_for('main.index'))

    if f.request.method == 'POST':
        email = f.request.form['email']
        unhashed_password = f.request.form['password']
        password = Util.hash_password(unhashed_password)
        user = User.query.filter_by(email=email).first()
        if user and user.password == password or user.password == unhashed_password:
            fl.login_user(user)
            next_page = f.request.args.get('next')
            return f.redirect(next_page) if next_page else f.redirect(f.url_for('main.index'))

    return f.render_template('users/login.jinja', title='Login')


@users_blueprint.route("/logout")
@fl.login_required
def logout():
    fl.logout_user()
    return f.redirect(f.url_for('main.index'))


@users_blueprint.route("/register", methods=['get', 'post'])
def register():
    template = f.render_template('users/register.jinja', title='Register')

    if fl.current_user.is_authenticated:
        return f.redirect(f.url_for('main.index'))

    if f.request.method == 'POST':
        email = f.request.form['email']
        unhashed_password = f.request.form['password']
        confirm_password = f.request.form['confirm']
        admin_password = f.request.form['admin_password']
        if unhashed_password != confirm_password or not email:
            return template

        if User.query.filter_by(email=email).first():
            return template

        if Util.hash_password(admin_password) == Util.hash_password(Config.SECRET_ADMIN_KEY):
            user = User(
                email=email,
                password=Util.hash_password(unhashed_password),
                roles_string=Config.ADMIN_ROLE
                )
        else:
            user = User(
                email=email,
                password=Util.hash_password(unhashed_password),
                )
        
        if user:
            db.session.add(user)
            db.session.commit()
            return f.redirect(f.url_for('main.index'))

    return template
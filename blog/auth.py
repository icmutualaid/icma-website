import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from blog.cli import init_cli
from blog.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


# associate the url /login with the login view function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user, error = retrieve_user(username, password)

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# associate the url /logout with the logout view function
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# register load_logged_in_user before the view function,
# no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db().cursor()
        db.execute(
            'SELECT * FROM blog_user WHERE id = (%s)', (user_id,)
        )
        g.user = db.fetchone()


# decorator to check for a login for actions that require it
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


# check credentials and return the user and any error message
def retrieve_user(username, password):
    db = get_db().cursor()

    error = None

    db.execute(
            'SELECT * FROM blog_user WHERE username = (%s)', (username,)
        )
    user = db.fetchone()

    print(username)
    print(user)

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    return user, error


def init_app(app):
    # define any cli commands
    init_cli(app)


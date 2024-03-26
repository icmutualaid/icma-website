import functools

import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

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
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


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
    db = get_db()

    error = None

    user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    return user, error


def create_user(db, username, password):
    db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
    db.commit()


# Register a cli command to manually add a blog user
@click.command('create-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_user_command(username, password):
    error = validate_credentials(username, password)

    # insert a user with these credentials
    if error is None:
        db = get_db()
        try:
            create_user(db, username, password)
            click.echo(f'Successfully registered user {username}.')
        except db.IntegrityError:
            click.echo(f'Error: User {username} is already registered.')
    else:
        click.echo(f'Error: {error}')


def init_app(app):
    # define the create-user cli command
    app.cli.add_command(create_user_command)


def validate_credentials(username, password):
    error = None
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    return error

import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.cli import with_appcontext
from sqlite3 import IntegrityError
import sys

from blog.db import get_db


bp = Blueprint('newsletter', __name__, url_prefix='/newsletter')


# associate the url /signup with the signup view function
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']

        try:
            create_user_email(email)
            session.clear()
            session['user_email'] = email
            return redirect(url_for('index'))
        except IntegrityError as e:
            flash('You have already signed up for our newsletter. Thank you! '
                  'If you are not receiving our emails, please check your '
                  'spam folder and contact us if you cannot find them.')
            print(e, file=sys.stderr)
            return render_template('newsletter/signup.html')
        except Exception as e:
            flash('An error occurred while trying to subscribe to our '
                  'newsletter. You have not been added to our email list. '
                  'Please contact us and let us know about the problem.')
            print(e, file=sys.stderr)
            return render_template


# register load_logged_in_user before the view function,
# no matter what URL is requested
@bp.before_app_request
def load_user_email():
    user_email = session.get('user_email')

    if user_email is None:
        g.user_email = None
    else:
        g.user_email = get_db().execute(
            'SELECT * FROM user_email WHERE email = ?', (user_email,)
        ).fetchone()


# return the user_email and any error message
def retrieve_user_email(email):
    db = get_db()

    error = None

    user_email = db.execute(
            'SELECT * FROM user_email WHERE email = ?', (email,)
        ).fetchone()

    if user_email is None:
        error = 'Email not found.'

    return user_email, error


def create_user_email(email):
    db = get_db()
    db.execute(
                    'INSERT INTO user_email (email) VALUES (?)',
                    ([email])
                )
    db.commit()


# Register a cli command to manually add a user_email
@click.command('create-user-email')
@click.argument('email')
@with_appcontext
def create_user_email_command(email):
    error = validate_credentials(email)

    # insert a user_email with these credentials
    if error is None:
        db = get_db()
        print(db)
        try:
            create_user_email(db, email)
            click.echo(f'Successfully signed up email {email}.')
        except db.IntegrityError:
            click.echo(f'Error: Email {email} is already signed up.')
    else:
        click.echo(f'Error: {error}')


def init_app(app):
    # define the create-user-email cli command
    app.cli.add_command(create_user_email_command)


def validate_credentials(email):
    error = None
    if not email:
        error = 'Email is required.'
    return error

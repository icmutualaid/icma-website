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
            create_newsletter_subscriber(email)
            session.clear()
            session['newsletter_subscriber'] = email
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
    newsletter_subscriber = session.get('newsletter_subscriber')

    if newsletter_subscriber is None:
        g.newsletter_subscriber = None
    else:
        g.newsletter_subscriber = get_db().execute(
            'SELECT * FROM newsletter_subscriber WHERE email = ?',
            (newsletter_subscriber,)
        ).fetchone()


# return the newsletter_subscriber and any error message
def retrieve_newsletter_subscriber(email):
    db = get_db()

    error = None

    newsletter_subscriber = db.execute(
            'SELECT * FROM newsletter_subscriber WHERE email = ?', (email,)
        ).fetchone()

    if newsletter_subscriber is None:
        error = 'Email not found.'

    return newsletter_subscriber, error


def create_newsletter_subscriber(email):
    db = get_db()
    db.execute(
                    'INSERT INTO newsletter_subscriber (email) VALUES (?)',
                    ([email])
                )
    db.commit()


# Register a cli command to manually add a newsletter_subscriber
@click.command('create-user-email')
@click.argument('email')
@with_appcontext
def create_newsletter_subscriber_command(email):
    error = validate_credentials(email)

    # insert a newsletter_subscriber with these credentials
    if error is None:
        db = get_db()
        print(db)
        try:
            create_newsletter_subscriber(db, email)
            click.echo(f'Successfully signed up email {email}.')
        except db.IntegrityError:
            click.echo(f'Error: Email {email} is already signed up.')
    else:
        click.echo(f'Error: {error}')


def init_app(app):
    # define the create-newsletter-subscriber cli command
    app.cli.add_command(create_newsletter_subscriber_command)


def validate_credentials(email):
    error = None
    if not email:
        error = 'Email is required.'
    return error

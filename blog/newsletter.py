import click
from flask import (
    Blueprint, flash, render_template, request, session
)
from flask.cli import with_appcontext
# from sqlite3 import IntegrityError
import sys

from blog.db import get_db


bp = Blueprint('newsletter', __name__, url_prefix='/newsletter')


# associate the url /signup with the signup view function
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']

        try:
            create_newsletter_subscriber(get_db(), email)
            session.clear()
            session['newsletter_subscriber'] = email
            flash('You have successfully signed up for our newsletter. '
                  'Thank you!')
        # except IntegrityError as e:
        #     flash('You have already signed up for our newsletter. Thank you! '
        #           'If you are not receiving our emails, please check your '
        #           'spam folder and contact us if you cannot find them.')
        #     print(e, file=sys.stderr)
        except Exception as e:
            flash('An error occurred while trying to subscribe to our '
                  'newsletter. Please check your spam folder and see if you '
                  'are already receiving our emails. Otherwise, please '
                  'contact us and let us know about the problem.')
            print(e, file=sys.stderr)

    return render_template('newsletter/signup.html')


# return the newsletter_subscriber and any error message
def retrieve_newsletter_subscriber(email):
    db = get_db().cursor()

    error = None

    db.execute(
            'SELECT * FROM newsletter_subscriber WHERE email = (%s)', (email,)
        )
    newsletter_subscriber = db.fetchone()

    if newsletter_subscriber is None:
        error = 'Email not found.'

    return newsletter_subscriber, error


def create_newsletter_subscriber(db, email):
    db.cursor().execute(
            'INSERT INTO newsletter_subscriber (email) VALUES ((%s))',
            (email,)
        )
    db.commit()


# Register a cli command to manually add a newsletter_subscriber
@click.command('create-newsletter-subscriber')
@click.argument('email')
@with_appcontext
def create_newsletter_subscriber_command(email):
    error = validate_credentials(email)

    # insert a newsletter_subscriber with these credentials
    if error is None:
        db = get_db().cursor()
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

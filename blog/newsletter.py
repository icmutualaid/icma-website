from flask import (
    Blueprint, current_app, flash, render_template, session
)
from flask_wtf import FlaskForm, RecaptchaField
import sys
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from blog.db import get_db
from psycopg2 import IntegrityError

bp = Blueprint('newsletter', __name__, url_prefix='/newsletter')


class NewsletterSignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')
    captcha = RecaptchaField()

    def __init__(self, app, *args, **kwargs):
        super(NewsletterSignupForm, self).__init__(*args, **kwargs)

        if app.debug or app.config.get('TESTING'):
            self.captcha.validators = []
            self.captcha.label = '''
                This site is running in debug mode,
                or automated tests are being run.
                Solving the reCAPTCHA is not required.
                '''


# associate the url /signup with the signup view function
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = NewsletterSignupForm(current_app)
    if form.validate_on_submit():
        email = form.email.data
        try:
            create_newsletter_subscriber(get_db(), email)
            session.clear()
            session['newsletter_subscriber'] = email
            flash('You have successfully signed up for our newsletter. '
                  'Thank you!')
        except IntegrityError:
            flash('An error occurred while trying to subscribe to our '
                  'newsletter. This is likely because your email is '
                  'already on our list. Please check your spam folder. '
                  'If you still are not receiving our emails, please '
                  'contact us and let us know.')
        except Exception as e:
            flash('An error occurred while trying to subscribe to our '
                  'newsletter. Please let us know about this problem!')
            print(e, file=sys.stderr)

    return render_template('newsletter/signup.html', form=form)


@bp.route('/', methods=('GET', 'POST'))
def index():
    # Allow posting/getting the signup form at the blueprint root
    return signup()


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

from flask import (
    Blueprint, flash, render_template, session
)
from flask_wtf import RecaptchaField
from flask_wtf import FlaskForm
# from sqlite3 import IntegrityError
import sys
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from blog.db import get_db

bp = Blueprint('newsletter', __name__, url_prefix='/newsletter')


class NewsletterSignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    captcha = RecaptchaField()
    submit = SubmitField('Sign Up')


@bp.route('/', methods=('GET', 'POST'))
# deprecated; kept here in case someone has bookmarked it
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = NewsletterSignupForm()
    if form.validate_on_submit():
        email = form.email.data
        try:
            create_newsletter_subscriber(get_db(), email)
            session.clear()
            session['newsletter_subscriber'] = email
            flash('You have successfully signed up for our newsletter. '
                  'Thank you!')
        except Exception as e:
            flash('An error occurred while trying to subscribe to our '
                  'newsletter. Please check your spam folder and see if you '
                  'are already receiving our emails. Otherwise, please '
                  'contact us and let us know about the problem.')
            print(e, file=sys.stderr)

    return render_template('newsletter/signup.html', form=form)


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

import psycopg2
import psycopg2.extras
# g is a special object that is unique for each request
# it stores request data that we might want to access
# in multiple places for the same request
from flask import current_app, g


# creates and returns the db cursor
def get_db():
    # cache the db connection as g.db
    # in case we call get_db multiple times for the same request
    if 'db' not in g:
        g.db = psycopg2.connect(
            current_app.config['DATABASE_URL'],
            # sslmode='require',
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    return g.db


# closes the db connection
# the application factory will call close_db after each request
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    # after each request, close that request's db connection
    app.teardown_appcontext(close_db)


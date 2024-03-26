import sqlite3

import click
# g is a special object that is unique for each request
# it is used to store data that might be accessed by multiple functions during the request
from flask import current_app, g


# creates and returns the db connection
def get_db():
    # cache the db connection as g.db in case we call get_db multiple times for the same request
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# closes the db connection
# the application factory will call close_db after each request
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# execute schema.sql, which drops and recreates our tables
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    # after each request, close that request's db connection
    app.teardown_appcontext(close_db)
    # define the init-db cli command
    app.cli.add_command(init_db_command)


# defines a cli command init-db
@click.command('init-db')
# clear the existing data and create new tables
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

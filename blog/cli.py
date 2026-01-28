import click
from flask.cli import with_appcontext
from psycopg2 import IntegrityError, ProgrammingError
from werkzeug.security import generate_password_hash

from blog.db import get_db


def init_cli(app):
    app.cli.add_command(create_user_command)


def create_user(db, username, password):
    cursor = db.cursor()
    cursor.execute(
            'INSERT INTO blog_user (username, password) '
            'VALUES ((%s), (%s))',
            (username, generate_password_hash(password)),
        )
    return db.commit()


# Register a cli command to manually add a blog user
@click.command('create-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_user_command(username, password):
    error = validate_create_user_params(username, password)

    # insert a user with these credentials
    if error is None:
        db = get_db()
        print(db)
        try:
            create_user(db, username, password)
            click.echo(f'OK: Successfully registered user {username}')
        except ProgrammingError as e:
            click.echo(f'Error: {e}')
        except IntegrityError:
            click.echo(f'Error: User {username} is already registered')
    else:
        click.echo(f'Error: {error}')


def validate_create_user_params(username, password):
    error = None
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    return error

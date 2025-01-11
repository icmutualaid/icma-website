import datetime
import psycopg2
import psycopg2.extras

import click
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


# execute schema.sql, which drops and recreates our tables
def init_db():
    db = get_db()

    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))


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


# # Add some recipes for adapters and converters.
# # The default sqlite3 timestamp converter is deprecated.
# def adapt_date_iso(val):
#     """Adapt datetime.date to ISO 8601 date."""
#     return val.isoformat()


# def adapt_datetime_iso(val):
#     """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
#     return val.isoformat()


# def adapt_datetime_epoch(val):
#     """Adapt datetime.datetime to Unix timestamp."""
#     return int(val.timestamp())


# sqlite3.register_adapter(datetime.date, adapt_date_iso)
# sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
# sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)


# def convert_date(val):
#     """Convert sqlite date bytestring to datetime.date object."""
#     return convert_datetime(val).date()


# def convert_datetime(val):
#     """Convert sqlite datetime bytestring to datetime.datetime object."""
#     return sql_time_bytes_to_datetime(val)


# def convert_timestamp(stamp: int | bytes) -> datetime.datetime:
#     """Convert Unix epoch timestamp to datetime.datetime object."""
#     # sqlite3 documentation says we should expect an epoch time in seconds.
#     # But it seems we actually get a datetime bytestring back from the db.
#     # So we should make sure we handle both cases.
#     # Perhaps this is version-specific???
#     if (type(stamp) is int):
#         return datetime.datetime.fromtimestamp(stamp)
#     if (type(stamp) is bytes):
#         return convert_datetime(stamp)
#     raise TypeError('convert_timestamp: invalid argument type '
#                     '(expected int or bytes)')


# # Convert an epoch time into a datetime
# def sql_time_bytes_to_datetime(t):
#     return datetime.datetime.strptime(t.decode(), '%Y-%m-%d %H:%M:%S')


# sqlite3.register_converter("date", convert_date)
# sqlite3.register_converter("datetime", convert_datetime)
# sqlite3.register_converter("timestamp", convert_timestamp)

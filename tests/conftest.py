import os

import pytest
from blog import create_app
from blog.db import get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    test_setup_sql = f.read().decode('utf8')


# The app fixture will call the factory
# and pass test_config to configure the application and database for testing
# instead of using our local development configuration.
@pytest.fixture
def app():
    db_url = os.getenv('DATABASE_URL')

    if not db_url:
        raise RuntimeError(
            'Set DATABASE_URL to a Postgres URL before running tests.'
        )

    app = create_app({
        'TESTING': True,
        'DATABASE_URL': db_url,
    })

    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(test_setup_sql)
        db.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# For most of the views, a user needs to be logged in.
# The easiest way to do this in tests is to make a POST request
# to the login view with the client.
# Rather than writing that out every time,
# we can write a class with methods to do that,
# and use a fixture to pass it the client for each test.
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='TEST', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


# With the auth fixture, we can call auth.login() in a test
# to log in as the test user, which was inserted
# as part of the test data in the app fixture.
@pytest.fixture
def auth(client):
    return AuthActions(client)

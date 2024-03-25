import pytest
from flask import g, session

from blog.auth import create_user_command


# The create-user command should call create_user function and echo a message.
def test_create_user_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_create_user():
        Recorder.called = True

    monkeypatch.setattr('blog.auth.create_user', fake_create_user)
    result = runner.invoke(
        args=['create-user', 'testusername', 'testpassword']
        )
    assert 'Successfully registered' in result.output
    assert Recorder.called


# Invalid data should display error messages.
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Username is required.'),
    ('a', '', 'Password is required.'),
    ('test', 'test', 'already registered'),
))
def test_validate_credentials(client, username, password, message):
    validation_message = create_user_command(username, password)
    assert message in validation_message


# The tests for the login view are very similar to those for register.
# Rather than testing the data in the database,
# session should have user_id set after logging in.
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


# Testing logout is the opposite of login:
# session should not contain user_id after logging out.
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

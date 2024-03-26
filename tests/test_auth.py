import pytest
from flask import g, session

# from blog.auth import create_user_command


# The create-user command should call create_user iff it has valid params.
# Invalid data should display error messages.
@pytest.mark.parametrize(('username', 'password', 'message', 'called'), (
    ('testuser', 'testpass', 'Successfully registered', True),
    ('', '', 'Username is required.', False),
    ('a', '', 'Password is required.', False),
    ('test', 'test', 'already registered', True),
))
def test_create_user(runner, monkeypatch, app,
                     username, password, message, called):
    class Recorder(object):
        called = False

    def fake_create_user(db, username, password):
        Recorder.called = True
        if username == 'test':
            raise db.IntegrityError('This user already exists')

    monkeypatch.setattr('blog.auth.create_user', fake_create_user)

    with app.app_context():
        result = runner.invoke(
            args=['create-user', username, password]
            )

    assert message in result.output
    assert called is Recorder.called


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

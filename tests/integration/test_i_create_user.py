import pytest


# The create-user command should call create_user iff it has valid params.
# Invalid data should display error messages.
@pytest.mark.parametrize(('username', 'password', 'message', 'called'), (
    ('testuser', 'testpass', 'Successfully registered', True),
    ('', '', 'Username is required.', False),
    ('a', '', 'Password is required.', False),
    ('TEST', 'test', 'already registered', True),
))
def test_integration_create_user(runner, monkeypatch, app,
                                 username, password, message, called):
    class Recorder(object):
        called = False

    def fake_create_user(db, username, password):
        Recorder.called = True
        if username == 'TEST':
            raise db.IntegrityError('This user already exists')

    monkeypatch.setattr('blog.cli.create_user', fake_create_user)

    with app.app_context():
        result = runner.invoke(
            args=['create-user', username, password]
            )

    assert message in result.output
    assert called is Recorder.called

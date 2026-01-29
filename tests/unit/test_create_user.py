import pytest
from werkzeug.security import check_password_hash

from blog.cli import create_user


class CreateUserTester(object):
    def __init__(self, expect_user, expect_password):
        self._cursor = CreateUserMockCursor(self)
        self.expect_user = expect_user
        self.expect_password = expect_password
        self.given_user = None
        self.given_password = None
        self.called_execute = False
        self.called_commit = False

    def _execute(self, sql, credentials):
        self.called_execute = True
        self.given_sql = sql
        self.given_user = credentials[0]
        self.given_password = credentials[1]

    def cursor(self):
        return self._cursor

    def commit(self):
        self.called_commit = True


class CreateUserMockCursor(object):
    def __init__(self, tester):
        self.tester = tester

    def execute(self, sql, credentials):
        self.tester._execute(sql, credentials)


@pytest.fixture
def cu_tester():
    username = 'test-user'
    password = 'Password123'
    tester = CreateUserTester(username, password)
    create_user(tester, username, password)
    return tester


def test_called_db_functions(cu_tester):
    assert cu_tester.called_execute
    assert cu_tester.called_commit


def test_passed_correct_execute_params(cu_tester):
    assert cu_tester.given_sql.startswith('insert into blog_user '
                                          '(username, password)')
    assert cu_tester.given_user == cu_tester.expect_user
    assert check_password_hash(cu_tester.given_password,
                               cu_tester.expect_password)


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

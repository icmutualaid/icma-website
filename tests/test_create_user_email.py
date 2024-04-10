import pytest

from blog.newsletter import create_user_email


class CreateUserEmailTester(object):
    def __init__(self, expect_email):
        self.expect_email = expect_email
        self.given_email = None
        self.called_execute = False
        self.called_commit = False

    def execute(self, sql, given_email):
        self.called_execute = True
        self.given_sql = sql
        self.given_email = given_email

    def commit(self):
        self.called_commit = True


@pytest.fixture
def cu_tester():
    email = 'testemail'
    tester = CreateUserEmailTester(email)
    create_user_email(tester, email)
    return tester


def test_called_db_functions(cu_tester):
    assert cu_tester.called_execute
    assert cu_tester.called_commit


def test_passed_correct_execute_params(cu_tester):
    assert cu_tester.given_sql.startswith('INSERT INTO user_email '
                                          '(email)')
    assert cu_tester.given_email == cu_tester.expect_email


# The create-user command should call create_user iff it has valid params.
# Invalid data should display error messages.
@pytest.mark.parametrize(('email', 'message', 'called'), (
    ('testemail', 'Successfully signed up', True),
    ('', 'Email is required.', False),
    ('test', 'already signed up', True),
))
def test_integration_create_user_email(runner, monkeypatch, app,
                                       email, message, called):
    class Recorder(object):
        called = False

    def fake_create_user_email(db, email):
        Recorder.called = True
        if email == 'test':
            raise db.IntegrityError('This email is already signed up')

    monkeypatch.setattr('blog.newsletter.create_user_email',
                        fake_create_user_email)

    with app.app_context():
        result = runner.invoke(
            args=['create-user-email', email]
            )

    assert message in result.output
    assert called is Recorder.called

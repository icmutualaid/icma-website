# import pytest

# from blog.newsletter import create_newsletter_subscriber

# from sqlite3 import IntegrityError


# class CreateNewsletterSubscriberTester(object):
#     def __init__(self, expect_email):
#         self.expect_email = expect_email
#         self.given_email = None
#         self.called_execute = False
#         self.called_commit = False

#     def execute(self, sql, given_params):
#         self.called_execute = True
#         self.given_sql = sql
#         self.given_email = given_params[0]

#     def commit(self):
#         self.called_commit = True


# @pytest.fixture
# def cu_tester():
#     email = 'testemail'
#     tester = CreateNewsletterSubscriberTester(email)
#     create_newsletter_subscriber(tester, email)
#     return tester


# def test_called_db_functions(cu_tester):
#     assert cu_tester.called_execute
#     assert cu_tester.called_commit


# def test_passed_correct_execute_params(cu_tester):
#     assert cu_tester.given_sql.startswith('INSERT INTO newsletter_subscriber '
#                                           '(email)')
#     assert cu_tester.given_email == cu_tester.expect_email


# # The create-newsletter-subscriber command should call
# # create_newsletter_subscriber iff it has valid params.
# # Invalid data should display error messages.
# @pytest.mark.parametrize(('email', 'message', 'called'), (
#     ('testemail', 'Successfully signed up', True),
#     ('', 'Email is required.', False),
#     ('test', 'already signed up', True),
# ))
# def test_integration_create_newsletter_subscriber(runner, monkeypatch, app,
#                                                   email, message, called):
#     class Recorder(object):
#         called = False

#     def fake_create_newsletter_subscriber(_, email):
#         Recorder.called = True
#         if email == 'test':
#             raise IntegrityError('This email is already signed up')

#     monkeypatch.setattr('blog.newsletter.create_newsletter_subscriber',
#                         fake_create_newsletter_subscriber)

#     with app.app_context():
#         result = runner.invoke(
#             args=['create-newsletter-subscriber', email]
#             )

#     assert message in result.output
#     assert called is Recorder.called

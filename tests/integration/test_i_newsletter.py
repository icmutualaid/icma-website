import pytest
from blog.db import get_db


# The signup form should return 200 OK
# and show the correct content.
def test_signup_get(client):
    response = client.get('/newsletter/signup')
    assert response.status_code == 200
    assert b'<h2>Sign up for our mailing list</h2>' in response.data


# When valid data is POSTed to signup, the new email should
# be added to the database.
def test_signup_post_ok(client, app):
    response = client.post('/newsletter/signup',
                           data={'email': 'newuser@test.com'})

    assert response.status_code == 200
    assert b'You have successfully signed up' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(email) '
                           'FROM newsletter_subscriber').fetchone()[0]
        assert count == 2


# When a duplicate email is submitted, the email should not be added
# to the database, and the form should flash a descriptive error.
def test_signup_post_duplicate(client, app):
    post_url = '/newsletter/signup'
    post_data = {'email': 'newuser@test.com'}

    client.post(post_url, data=post_data)
    response = client.post(post_url, data=post_data)

    assert response.status_code == 200
    assert b'You have already signed up' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(email) '
                           'FROM newsletter_subscriber').fetchone()[0]
        assert count == 2

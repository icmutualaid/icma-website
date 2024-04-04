# Test static content pages (blog/content.py, blog/templates/content/)

def test_about(client, auth):
    response = client.get('/about')
    assert b'<h1>About' in response.data


def test_projects(client, auth):
    response = client.get('/projects')
    assert b'<h1>Projects' in response.data


def test_resources(client, auth):
    response = client.get('/resources')
    assert b'<h1>Resources' in response.data

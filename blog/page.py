from flask import (
    abort, Blueprint, render_template,
)
from blog.auth import login_required
from blog.blog import index as blog_index
from blog.db import get_db


# Routing for static content pages (about, projects, resources)
bp = Blueprint('page', __name__)


# We will use the page index to route anything not specifically
# handled by something else.
@bp.route('/<_path>')
def index(_path):
    # If we are literally at /, return the blog index.
    if (_path == '/' or _path == 'index' or _path == ''):
        return blog_index()
    page_match = get_db().execute("""
                                  SELECT path
                                  FROM page
                                  WHERE path = ?
                                  """,
                                  [_path]).fetchone()
    if page_match is not None:
        return render_template('page/index.html', page=page_match)
    abort(404)


# Create a new page (about, projects, resources)
@bp.route('/page/create', methods=('GET', 'POST'))
@login_required
def create():
    return render_template('page/create.html')


@bp.route('/page/update', methods=('GET', 'POST'))
def update():
    raise Exception('Not yet implemented')


# retrieve a post with the given id
# check_author is True if a request needs authentication, e.g., editing a post
def get_page(path, check_author=True):
    page = get_db().execute(
        """
        SELECT path, title, body, created, author_id, username
        FROM page p JOIN user u ON p.author_id = u.id
        WHERE path = ?
        """,
        (path,)
    ).fetchone()

    if page is None:
        abort(404, f"Post id {id} doesn't exist.")

    # abort raises an exception, so we now know that page is not None
    if check_author and page['author_id'] != g.user['id']:
        abort(403)

    return page


class Page:
    def __init__(self, path):
        self.path = path


class NavPage(Page):
    def __init__(self, path, top_nav):
        self.top_nav = top_nav
        super(NavPage, self).__init__(path)


def top_nav():
    nav_result = get_db().execute("""
                                  SELECT path, top_nav
                                  FROM page
                                  WHERE top_nav IS NOT NULL
                                  """).fetchall()
    rows = (dict(row) for row in nav_result)
    return (NavPage(row['path'], row['top_nav']) for row in rows)


# def rebuild(app):

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import flask_ckeditor

from blog.auth import login_required
from blog.db import get_db


# Polyfill for flask_ckeditor.utils.cleanify
# Stolen from https://github.com/helloflask/flask-ckeditor/
# Can be replaced with an import when flask_ckeditor==0.5.2 is released:
# from flask_ckeditor.utils import cleanify
# Then we can also remove the bleach dependency.
def cleanify(text, *, allow_tags=None):
    import bleach
    """Clean the input from client, this function rely on bleach.

    :parm text: input str
    :parm allow_tags: if you don't want to use default `allow_tags`,
        you can provide a Iterable which include html tag string like ['a', 'li',...].
    """
    default_allowed_tags = {'a', 'abbr', 'b', 'blockquote', 'code',
                            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'}
    return bleach.clean(text, tags=allow_tags or default_allowed_tags)


bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = cleanify(
                        request.form.get('body'),
                        allow_tags={
                            'p',
                            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                            'a',
                            'abbr',
                            'blockquote',
                            'b', 'strong', 'i', 'em', 'u',
                            'pre', 'code',
                            'ul', 'ol', 'li',
                            'table', 'tr', 'tbody', 'td', 'thead', 'th',
                            'img',
                            },
                        )
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# retrieve a post with the given id
# check_author is True if a request needs authentication, e.g., editing a post
def get_post(id, check_author=True):
    post = get_db().execute(
        """
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.id = ?
        """,
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    # abort raises an exception, so we now know that post is not None
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

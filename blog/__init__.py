import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    _init_config(app, test_config)

    _init_instance(app)
    _init_db(app)

    _init_route(app)

    return app



# ensure the instance folder exists
def _init_instance(app):
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def _init_config(app, test_config):
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


# register the db
def _init_db(app):
    from . import db
    db.init_app(app)


# route the request
def _init_route(app):
    # hello world page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the auth blueprint with a url prefix defined in auth.py
    from . import auth
    app.register_blueprint(auth.bp)

    # register the blog blueprint at the site root
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
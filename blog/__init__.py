import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    _init_config(app, test_config)

    _init_instance(app)
    _init_db(app)
    _init_auth(app)

    _init_routing(app)

    return app


def _init_auth(app):
    from . import auth
    app.register_blueprint(auth.bp)

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
def _init_routing(app):
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

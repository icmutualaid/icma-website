from flask import (
    Blueprint, render_template
)


bp = Blueprint('content', __name__)


# Routing for static content pages (about, projects, resources)
@bp.route('/about')
def about():
    return render_template('content/about.html')


@bp.route('/projects')
def projects():
    return render_template('content/projects.html')


@bp.route('/resources')
def resources():
    return render_template('content/resources.html')

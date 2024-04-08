from dominate import tags
from flask import g
from flask_nav3 import Nav, register_renderer
from flask_nav3.elements import Navbar, View
from flask_nav3.renderers import Renderer, SimpleRenderer

from blog.page import top_nav as get_dynamic_pages

nav = Nav()


def configure_navbar(app):
    nav.register_element('top_nav', top_nav)
    register_renderer(app, 'custom', SimpleRenderer)
    nav.init_app(app)
    return app


def top_nav():
    log_link = IconView('Log Out', 'auth.logout',
                        'fa-solid fa-right-from-bracket') if g.user \
        else IconView('Log In', 'auth.login',
                      'fa-solid fa-right-to-bracket')
    items = (
        *(View(page.top_nav, page.path) for page in get_dynamic_pages()),
        # View('Newsletter', 'newsletter.signup'),
        log_link,
    )
    return Navbar('top_nav', *items)


class IconView(View):
    def __init__(self, text, endpoint, icon_class, **kwargs):
        self.icon_class = icon_class
        self.text = text
        self.endpoint = endpoint
        self.url_for_kwargs = kwargs


class CustomRenderer(Renderer):
    def visit_Navbar(self, node):
        sub = []
        for item in node.items:
            sub.append(self.visit(item))

        return tags.ul('Navigation:', _class='navbar', *sub)

    def visit_View(self, node):
        return tags.li('{} ({})'.format(node.title, node.get_url()))

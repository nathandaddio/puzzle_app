from pyramid.config import Configurator

from pyramid.request import Request
from pyramid.request import Response


def request_factory(environ):
    request = Request(environ)
    if request.is_xhr:
        print("Made it")

        request.response = Response()
        request.response.headerlist = []
        request.response.headerlist.extend(
            (
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'application/json')
            )
        )
    return request


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_celery')
    config.configure_celery(global_config['__file__'])
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.set_request_factory(request_factory)
    config.scan()

    return config.make_wsgi_app()

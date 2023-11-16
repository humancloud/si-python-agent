#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response


def index(request):
    return Response('Hello World!')


def error(request):
    raise Exception('Error!')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('pyramid', '/pyramid')
        config.add_route('error', '/error')
        config.add_view(index, route_name='pyramid')
        config.add_view(error, route_name='error')

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 9091, app)

    server.serve_forever()

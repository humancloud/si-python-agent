#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from urllib import request
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response


def index(req):
    data = '{"name": "whatever"}'.encode('utf8')
    req = request.Request(f'http://provider:9091/{req.path.lstrip("/")}')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', str(len(data)))
    with request.urlopen(req, data):
        return Response(data)


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('pyramid', '/pyramid')
        config.add_view(index, route_name='pyramid')

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 9090, app)

    server.serve_forever()

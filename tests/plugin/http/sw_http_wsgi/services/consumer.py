#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from urllib import request


if __name__ == '__main__':
    import socketserver
    from http.server import BaseHTTPRequestHandler

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            data = '{"name": "whatever"}'.encode('utf8')
            req = request.Request('http://provider:9091/users')
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req.add_header('Content-Length', str(len(data)))
            with request.urlopen(req, data):
                self.wfile.write(data)

    PORT = 9090
    Handler = SimpleHTTPRequestHandler

    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print('serving at port', PORT)
        httpd.serve_forever()

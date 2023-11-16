#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import requests


if __name__ == '__main__':
    import socketserver
    from http.server import BaseHTTPRequestHandler

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            res = requests.post('http://provider:9091/users', timeout=5)
            self.wfile.write(str(res.json()).encode('utf8'))

    PORT = 9090
    Handler = SimpleHTTPRequestHandler

    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print('serving at port', PORT)
        httpd.serve_forever()

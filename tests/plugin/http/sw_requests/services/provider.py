#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time


if __name__ == '__main__':
    import socketserver
    from http.server import BaseHTTPRequestHandler

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def do_POST(self):  # noqa
            time.sleep(0.5)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write('{"song": "Despacito", "artist": "Luis Fonsi"}'.encode('ascii'))

    PORT = 9091
    Handler = SimpleHTTPRequestHandler

    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()

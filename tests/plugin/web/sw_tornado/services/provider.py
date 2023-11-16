#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

if __name__ == '__main__':
    import json
    import time

    import tornado.ioloop
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            time.sleep(0.5)
            self.write(json.dumps({'song': 'Despacito', 'artist': 'Luis Fonsi'}))

    def make_app():
        return tornado.web.Application([
            (r'/users', MainHandler),
        ])

    app = make_app()
    app.listen(9091, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()

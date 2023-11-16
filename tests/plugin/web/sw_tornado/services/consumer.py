#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

if __name__ == '__main__':
    import requests
    import tornado.ioloop
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            res = requests.get('http://provider:9091/users', timeout=5)
            self.write(res.text)

    def make_app():
        return tornado.web.Application([
            (r'/users', MainHandler),
        ])

    app = make_app()
    app.listen(9090, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()

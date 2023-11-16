#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import requests

from stackinsights.decorators import runnable

if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        from stackinsights.trace.context import get_context
        get_context().put_correlation('correlation', 'correlation')

        @runnable(op='/test')
        def post():
            requests.post('http://provider:9091/users', timeout=5)

        from threading import Thread
        t = Thread(target=post)
        t.start()

        res = requests.post('http://provider:9091/users', timeout=5)

        t.join()

        return jsonify(res.json())

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)

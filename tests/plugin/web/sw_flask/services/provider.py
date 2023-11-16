#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time


if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        from stackinsights.trace.context import get_context
        time.sleep(0.5)
        return jsonify({'correlation': get_context().get_correlation('correlation')})

    PORT = 9091
    app.run(host='0.0.0.0', port=PORT, debug=True)

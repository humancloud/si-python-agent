#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import requests


if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        res = requests.post('http://provider:9091/users', timeout=5)
        return jsonify(res.json())

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)

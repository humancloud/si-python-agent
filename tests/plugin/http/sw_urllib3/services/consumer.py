#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import json


if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)
    import urllib3

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        http = urllib3.PoolManager()
        res = http.request('POST', 'http://provider:9091/users')

        return jsonify(json.loads(res.data.decode('utf-8')))

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)

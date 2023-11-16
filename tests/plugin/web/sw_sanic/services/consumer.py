#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import requests

if __name__ == '__main__':
    from sanic import Sanic, response

    app = Sanic(__name__)

    @app.route('/users', methods=['GET'])
    async def application(req):
        res = requests.get('http://provider:9091/users', timeout=5)
        return response.json(res.json())

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)

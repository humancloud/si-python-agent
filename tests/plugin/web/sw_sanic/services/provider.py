#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time

if __name__ == '__main__':
    from sanic import Sanic, response

    app = Sanic(__name__)

    @app.route('/users', methods=['GET'])
    async def application(req):
        time.sleep(0.5)
        return response.json(
            {'song': 'Despacito', 'artist': 'Luis Fonsi'}
        )

    PORT = 9091
    app.run(host='0.0.0.0', port=PORT)

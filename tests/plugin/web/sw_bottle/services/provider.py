#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time
import json
from bottle import route, run


if __name__ == '__main__':
    @route('/users', method='GET')
    @route('/users', method='POST')
    def hello():
        time.sleep(0.5)
        return json.dumps({'song': 'Despacito', 'artist': 'Luis Fonsi'})

    run(host='0.0.0.0', port=9091, debug=True)

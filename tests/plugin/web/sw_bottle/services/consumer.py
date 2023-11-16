#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import requests
from bottle import route, run


if __name__ == '__main__':
    @route('/users', method='GET')
    @route('/users', method='POST')
    def hello():
        res = requests.post('http://provider:9091/users', timeout=5)
        return res.json()

    run(host='0.0.0.0', port=9090, debug=True)

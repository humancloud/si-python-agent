#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time
import random
from flask import Flask, request

app = Flask(__name__)


@app.route('/artist-provider', methods=['POST'])
def artist():
    try:

        time.sleep(random.random())
        payload = request.get_json()
        print(f'args: {payload}')

        return {'artist': 'song'}
    except Exception as e:  # noqa
        return {'message': str(e)}


if __name__ == '__main__':
    # noinspection PyTypeChecker
    app.run(host='0.0.0.0', port=9090)

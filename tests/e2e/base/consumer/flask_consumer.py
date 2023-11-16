#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

"""
Used by uWSGI which doesn't support FASTAPI (ASGI).
"""
import time
import random
from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/artist-consumer', methods=['POST', 'GET'])
def artist():
    try:
        time.sleep(random.random())
        payload = request.get_json()
        requests.post('http://provider:9090/artist-provider', data=payload)

        return {'artist': 'song'}
    except Exception as e:  # noqa
        return {'message': str(e)}


if __name__ == '__main__':
    # noinspection PyTypeChecker
    app.run(host='0.0.0.0', port=9090)

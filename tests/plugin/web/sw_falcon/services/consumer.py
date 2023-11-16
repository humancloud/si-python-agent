#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import hug
import requests


@hug.get('/users')
def get():
    res = requests.get('http://provider:9091/users', timeout=5)
    return res.json()


hug.API(__name__).http.serve(port=9090)

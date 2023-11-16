#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import json
import time

import hug


@hug.get('/users')
def get():
    time.sleep(0.5)
    return json.dumps({'song': 'Despacito', 'artist': 'Luis Fonsi'})


hug.API(__name__).http.serve(port=9091)

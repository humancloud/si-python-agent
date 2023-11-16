#!/bin/sh

#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

set -ex
pip install gunicorn gevent "greenlet<2.0.0"
gunicorn -k gevent -b :9090 --chdir /services entrypoint:app

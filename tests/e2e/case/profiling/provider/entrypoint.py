#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from gevent import monkey
monkey.patch_all()
import grpc.experimental.gevent as grpc_gevent # noqa key point
grpc_gevent.init_gevent()  # noqa key point
from stackinsights import config, agent # noqa
config.agent_logging_level = 'DEBUG'
# config.init()
agent.start()

from provider import app  # noqa

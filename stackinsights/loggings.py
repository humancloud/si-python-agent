#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import logging

from stackinsights import config

logger_debug_enabled = False


def getLogger(name=None):  # noqa
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)s [pid:%(process)d] [%(threadName)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False

    return logger


logger = getLogger('stackinsights')


def init():
    global logger_debug_enabled
    logging.addLevelName(logging.CRITICAL + 10, 'OFF')
    logger.setLevel(logging.getLevelName(config.agent_logging_level))
    logger_debug_enabled = logger.isEnabledFor(logging.DEBUG)

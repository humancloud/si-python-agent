#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import logging
import traceback

from stackinsights.log import sw_logging
from stackinsights.loggings import logger


def install():
    logger.debug('Installing plugin for logging module')
    # noinspection PyBroadException
    try:
        sw_logging.install()
    except Exception:
        logger.warning('Failed to install sw_logging plugin')
        traceback.print_exc() if logger.isEnabledFor(logging.DEBUG) else None

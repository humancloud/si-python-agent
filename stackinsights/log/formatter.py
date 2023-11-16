#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import io
import logging
import traceback


class SWFormatter(logging.Formatter):
    """
    A slightly modified formatter that allows traceback depth
    """
    def __init__(self, fmt, tb_limit):
        logging.Formatter.__init__(self, fmt)
        self.tb_limit = tb_limit

    def formatException(self, ei):  # noqa
        """
        Format and return the specified exception information as a string.
        """
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, self.tb_limit, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == '\n':
            s = s[:-1]
        return s

    def format(self, record):
        """
        Bypass cache so we don't disturb other Formatters
        """
        _exc_text = record.exc_text
        record.exc_text = None
        result = super(SWFormatter, self).format(record)
        record.exc_text = _exc_text

        return result

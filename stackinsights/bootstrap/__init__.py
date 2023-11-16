#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

""" This sub-package is for the convenience of deployment and automation
A CLI for running Python scripts and programs with StackInsights Python Agent automatically attached.
`loader/sitecustomize.py` is invoked by the Python interpreter at startup.
"""

import logging


def get_cli_logger():
    """ A logger used by sw-python CLI """
    logger = logging.getLogger('stackinsights-cli')
    logger.setLevel('INFO')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False

    return logger


cli_logger = get_cli_logger()

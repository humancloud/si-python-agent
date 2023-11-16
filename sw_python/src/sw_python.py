#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

""" Just an entry point script
python -m sw_python -d run command
or just use the setup console script
sw-python run command after setup install
"""
from stackinsights.bootstrap.cli import sw_python


def start():
    sw_python.start()

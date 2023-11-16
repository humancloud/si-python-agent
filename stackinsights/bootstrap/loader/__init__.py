#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import os


def get_loader_path():
    """ Return the path of loader
    Don't use this in sitecustomize,
    Somehow returns a capitalized version, behaves differently.
    """

    return os.path.dirname(__file__)

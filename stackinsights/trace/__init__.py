#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import uuid

from stackinsights.utils.counter import AtomicCounter

_id = AtomicCounter()


class ID(object):
    def __init__(self, raw_id: str = None):
        self.value = raw_id or str(uuid.uuid1()).replace('-', '')

    def __str__(self):
        return self.value

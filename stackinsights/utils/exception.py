#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

class VersionRuleException(Exception):
    def __init__(self, message):
        self.message = message


class IllegalStateError(RuntimeError):
    """
    Raised when tracing context falls into unexpected state.
    """
    pass

#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import base64


def tostring(cls):
    def __str__(self): # noqa
        return f"{type(self).__name__}@{id(self)}[{', '.join(f'{k}={str(v)}' for (k, v) in vars(self).items())}]"
    cls.__str__ = __str__
    return cls


def b64encode(s: str = '') -> str:
    return base64.b64encode(s.encode('utf8')).decode('utf8')


def b64decode(s: str = '') -> str:
    return base64.b64decode(s).decode('utf8')

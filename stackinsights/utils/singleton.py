#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#


class Singleton(object):
    """
    This is to ensure a single process can only have one instance of agent.
    Written by Guido van Rossum to implement a singleton pattern.
    https://www.python.org/download/releases/2.2/descrintro/#__new__
    Classes that inherit from this class will be singletons.
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass

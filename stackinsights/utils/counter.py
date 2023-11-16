#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import threading


class Counter:
    def __init__(self):
        self.value = -1

    def next(self) -> int:
        self.value += 1
        return self.value

    def __str__(self):
        return str(self.value)


class AtomicCounter(Counter):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()

    def next(self) -> int:
        with self._lock:
            return Counter.next(self)

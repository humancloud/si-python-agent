#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import threading
import timeit
from enum import Enum
from stackinsights.meter.meter import BaseMeter, MeterType
from stackinsights.protocol.language_agent.Meter_pb2 import MeterData, MeterSingleValue


class CounterMode(Enum):
    INCREMENT = 1
    RATE = 2


class Counter(BaseMeter):
    def __init__(self, name: str, mode: CounterMode, tags=None):
        super().__init__(name, tags)
        self.count = 0
        self.previous = 0
        self.mode = mode
        self._lock = threading.Lock()

    def increment(self, value):
        with self._lock:
            self.count += value

    def get(self):
        return self.count

    def transform(self):
        current_value = self.get()
        if self.mode == CounterMode.RATE:
            count = current_value - self.previous
            self.previous = current_value
        else:
            count = current_value

        meterdata = MeterData(singleValue=MeterSingleValue(name=self.get_name(), labels=self.transform_tags(), value=count))
        return meterdata

    def get_type(self):
        return MeterType.COUNTER

    def create_timer(self):
        return Counter.Timer(self)

    class Timer():
        def __init__(self, metrics):
            self.metrics = metrics

        def __enter__(self):
            self.start = timeit.default_timer()

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.stop = timeit.default_timer()
            duration = self.stop - self.start
            self.metrics.increment(duration)

    @staticmethod
    def timer(name: str):
        def inner(func):
            def wrapper(*args, **kwargs):
                start = timeit.default_timer()
                func(*args, **kwargs)
                stop = timeit.default_timer()
                duration = stop - start
                counter = Counter.meter_service.get_meter(name)
                counter.increment(duration)

            return wrapper

        return inner

    @staticmethod
    def increase(name: str, num=1):
        def inner(func):
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
                counter = Counter.meter_service.get_meter(name)
                counter.increment(num)

            return wrapper

        return inner

    class Builder(BaseMeter.Builder):
        def __init__(self, name: str, mode: CounterMode, tags=None):
            self.meter = Counter(name, mode, tags)

        def mode(self, mode: CounterMode):
            self.meter.mode = mode
            return self

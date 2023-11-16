#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights.meter.meter import BaseMeter, MeterType
from stackinsights.protocol.language_agent.Meter_pb2 import MeterData, MeterSingleValue


class Gauge(BaseMeter):
    def __init__(self, name: str, generator, tags=None):
        super().__init__(name, tags)
        self.generator = generator

    def get(self):
        data = next(self.generator, None)
        return data if data else 0

    def transform(self):
        count = self.get()
        meterdata = MeterData(singleValue=MeterSingleValue(name=self.get_name(), labels=self.transform_tags(), value=count))
        return meterdata

    def get_type(self):
        return MeterType.GAUGE

    class Builder(BaseMeter.Builder):
        def __init__(self, name: str, generator, tags=None):
            self.meter = Gauge(name, generator, tags)

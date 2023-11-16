#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights.meter.gauge import Gauge


class DataSource:
    def register(self):
        for name in dir(self):
            if name.endswith('generator'):
                generator = getattr(self, name)()
                Gauge.Builder('instance_pvm_' + name[:-10], generator).build()

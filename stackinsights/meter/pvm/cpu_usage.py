#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import psutil
from stackinsights.meter.pvm.data_source import DataSource


class CPUUsageDataSource(DataSource):
    def __init__(self):
        self.cur_process = psutil.Process()

    def total_cpu_utilization_generator(self):
        while (True):
            yield psutil.cpu_percent()

    def process_cpu_utilization_generator(self):
        while (True):
            yield self.cur_process.cpu_percent()

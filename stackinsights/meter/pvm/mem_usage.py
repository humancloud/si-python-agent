#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights.meter.pvm.data_source import DataSource
import psutil


class MEMUsageDataSource(DataSource):
    def __init__(self):
        self.cur_process = psutil.Process()

    def total_mem_utilization_generator(self):
        while (True):
            yield psutil.virtual_memory().percent

    def process_mem_utilization_generator(self):
        while (True):
            yield self.cur_process.memory_info().rss / psutil.virtual_memory().total

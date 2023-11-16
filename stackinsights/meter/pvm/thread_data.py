#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import psutil
from stackinsights.meter.pvm.data_source import DataSource


class ThreadDataSource(DataSource):
    def __init__(self):
        self.cur_process = psutil.Process()

    def thread_active_count_generator(self):
        while (True):
            ps = [self.cur_process]
            count = 0

            while len(ps) > 0:
                p = ps[0]
                ps.pop(0)
                count += p.num_threads()
                ps += p.children()

            yield count

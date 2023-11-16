#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import gc
import time

from stackinsights.meter.pvm.data_source import DataSource


class GCDataSource(DataSource):
    def gc_g0_generator(self):
        while (True):
            yield gc.get_stats()[0]['collected']

    def gc_g1_generator(self):
        while (True):
            yield gc.get_stats()[1]['collected']

    def gc_g2_generator(self):
        while (True):
            yield gc.get_stats()[2]['collected']

    def gc_time_generator(self):
        self.gc_time = 0

        def gc_callback(phase, info):
            if phase == 'start':
                self.start_time = time.time()
            elif phase == 'stop':
                self.gc_time = (time.time() - self.start_time) * 1000

        if hasattr(gc, 'callbacks'):
            gc.callbacks.append(gc_callback)

        while (True):
            yield self.gc_time

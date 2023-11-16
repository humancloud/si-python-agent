#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import time
import asyncio

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from stackinsights import config
from stackinsights.agent import agent
from stackinsights.meter.meter import BaseMeter
from stackinsights.utils.time import current_milli_time
from stackinsights.loggings import logger


class MeterService(Thread):
    def __init__(self):
        super().__init__(name='meterService', daemon=True)
        logger.debug('Started meter service')
        self.meter_map = {}

    def register(self, meter: BaseMeter):
        self.meter_map[meter.get_id().get_name()] = meter

    def get_meter(self, name: str):
        return self.meter_map.get(name)

    def send(self):

        def archive(meterdata):
            meterdata = meterdata.transform()
            meterdata.service = config.agent_name
            meterdata.serviceInstance = config.agent_instance_name
            meterdata.timestamp = current_milli_time()
            agent.archive_meter(meterdata)

        with ThreadPoolExecutor(thread_name_prefix='meter_service_pool_worker', max_workers=1) as executor:
            executor.map(archive, self.meter_map.values())

    def run(self):
        while True:
            time.sleep(config.agent_meter_reporter_period)
            self.send()


class MeterServiceAsync():
    def __init__(self):
        self.meter_map = {}
        # strong reference to asyncio.Task to prevent garbage collection
        self.strong_ref_set = set()

    def register(self, meter: BaseMeter):
        self.meter_map[meter.get_id().get_name()] = meter

    def get_meter(self, name: str):
        return self.meter_map.get(name)

    async def send(self):

        async def archive_async(meterdata):
            meterdata = meterdata.transform()
            meterdata.service = config.agent_name
            meterdata.serviceInstance = config.agent_instance_name
            meterdata.timestamp = current_milli_time()
            await agent.archive_meter_async(meterdata)

        for m in self.meter_map.values():
            task = asyncio.create_task(archive_async(m))
            self.strong_ref_set.add(task)
            task.add_done_callback(self.strong_ref_set.discard)

    async def start(self):
        logger.debug('Started async meter service')
        while True:
            await asyncio.sleep(config.agent_meter_reporter_period)
            await self.send()

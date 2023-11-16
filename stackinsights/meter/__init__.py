#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import asyncio

_meter_service = None


def init(force: bool = False):
    """
    If the meter service is not initialized, initialize it.
    if force, we are in a fork(), we force re-initialization
    """
    from stackinsights.meter.meter_service import MeterService

    global _meter_service
    if _meter_service and not force:
        return

    _meter_service = MeterService()
    _meter_service.start()


async def init_async(async_event: asyncio.Event = None):
    from stackinsights.meter.meter_service import MeterServiceAsync

    global _meter_service

    _meter_service = MeterServiceAsync()
    if async_event is not None:
        async_event.set()
    task = asyncio.create_task(_meter_service.start())
    _meter_service.strong_ref_set.add(task)

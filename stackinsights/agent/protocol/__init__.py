#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from abc import ABC, abstractmethod
from queue import Queue
from asyncio import Queue as QueueAsync


class Protocol(ABC):
    @abstractmethod
    def heartbeat(self):
        raise NotImplementedError()

    @abstractmethod
    def report_segment(self, queue: Queue, block: bool = True):
        raise NotImplementedError()

    @abstractmethod
    def report_log(self, queue: Queue, block: bool = True):
        raise NotImplementedError()

    @abstractmethod
    def report_meter(self, queue: Queue, block: bool = True):
        raise NotImplementedError()

    @abstractmethod
    def report_snapshot(self, queue: Queue, block: bool = True):
        raise NotImplementedError()

    @abstractmethod
    def query_profile_commands(self):
        raise NotImplementedError()

    @abstractmethod
    def notify_profile_task_finish(self, task):
        raise NotImplementedError()


class ProtocolAsync(ABC):
    @abstractmethod
    async def heartbeat(self):
        raise NotImplementedError()

    @abstractmethod
    async def report_segment(self, queue: QueueAsync):
        raise NotImplementedError()

    @abstractmethod
    async def report_log(self, queue: QueueAsync):
        raise NotImplementedError()

    @abstractmethod
    async def report_meter(self, queue: QueueAsync):
        raise NotImplementedError()

    @abstractmethod
    async def report_snapshot(self, queue: QueueAsync):
        raise NotImplementedError()

    @abstractmethod
    async def query_profile_commands(self):
        raise NotImplementedError()

    @abstractmethod
    async def notify_profile_task_finish(self, task):
        raise NotImplementedError()

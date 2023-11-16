#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from queue import Queue, Empty
from time import time

from stackinsights import config
from stackinsights.agent import Protocol
from stackinsights.client.http import HttpServiceManagementClient, HttpTraceSegmentReportService, HttpLogDataReportService
from stackinsights.loggings import logger, logger_debug_enabled
from stackinsights.protocol.logging.Logging_pb2 import LogData
from stackinsights.trace.segment import Segment


class HttpProtocol(Protocol):
    def __init__(self):
        self.properties_sent = False
        self.service_management = HttpServiceManagementClient()
        self.traces_reporter = HttpTraceSegmentReportService()
        self.log_reporter = HttpLogDataReportService()

    def heartbeat(self):
        if not self.properties_sent:
            self.service_management.send_instance_props()
            self.properties_sent = True
        self.service_management.send_heart_beat()

    def report_segment(self, queue: Queue, block: bool = True):
        start = None

        def generator():
            nonlocal start

            while True:
                try:
                    timeout = config.agent_queue_timeout  # type: int
                    if not start:  # make sure first time through queue is always checked
                        start = time()
                    else:
                        timeout -= int(time() - start)
                        if timeout <= 0:  # this is to make sure we exit eventually instead of being fed continuously
                            return
                    segment = queue.get(block=block, timeout=timeout)  # type: Segment
                except Empty:
                    return

                queue.task_done()

                if logger_debug_enabled:
                    logger.debug('reporting segment %s', segment)

                yield segment

        try:
            self.traces_reporter.report(generator=generator())
        except Exception:
            pass

    def report_log(self, queue: Queue, block: bool = True):
        start = None

        def generator():
            nonlocal start

            while True:
                try:
                    timeout = config.agent_queue_timeout  # type: int
                    if not start:  # make sure first time through queue is always checked
                        start = time()
                    else:
                        timeout -= int(time() - start)
                        if timeout <= 0:  # this is to make sure we exit eventually instead of being fed continuously
                            return
                    log_data = queue.get(block=block, timeout=timeout)  # type: LogData
                except Empty:
                    return
                queue.task_done()
                if logger_debug_enabled:
                    logger.debug('Reporting Log')

                yield log_data

        try:
            self.log_reporter.report(generator=generator())
        except Exception:
            pass

    # meter support requires OAP side HTTP handler to be implemented
    def report_meter(self, queue: Queue, block: bool = True):
        ...

    def report_snapshot(self, queue: Queue, block: bool = True):
        ...

    def query_profile_commands(self):
        ...

    def notify_profile_task_finish(self, task):
        ...

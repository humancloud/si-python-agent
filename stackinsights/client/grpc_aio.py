#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import grpc

from stackinsights import config
from stackinsights.client import ServiceManagementClientAsync, TraceSegmentReportServiceAsync, \
    ProfileTaskChannelServiceAsync, LogDataReportServiceAsync, MeterReportServiceAsync
from stackinsights.command import command_service_async
from stackinsights.loggings import logger, logger_debug_enabled
from stackinsights.profile import profile_task_execution_service
from stackinsights.profile.profile_task import ProfileTask
from stackinsights.protocol.language_agent.Tracing_pb2_grpc import TraceSegmentReportServiceStub
from stackinsights.protocol.logging.Logging_pb2_grpc import LogReportServiceStub
from stackinsights.protocol.management.Management_pb2 import InstancePingPkg, InstanceProperties
from stackinsights.protocol.language_agent.Meter_pb2_grpc import MeterReportServiceStub
from stackinsights.protocol.management.Management_pb2_grpc import ManagementServiceStub
from stackinsights.protocol.profile.Profile_pb2 import ProfileTaskCommandQuery, ProfileTaskFinishReport
from stackinsights.protocol.profile.Profile_pb2_grpc import ProfileTaskStub


class GrpcServiceManagementClientAsync(ServiceManagementClientAsync):
    def __init__(self, channel: grpc.aio.Channel):
        super().__init__()
        self.instance_properties = self.get_instance_properties_proto()
        self.service_stub = ManagementServiceStub(channel)

    async def send_instance_props(self):
        await self.service_stub.reportInstanceProperties(InstanceProperties(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            properties=self.instance_properties,
        ))

    async def send_heart_beat(self):
        await self.refresh_instance_props()

        await self.service_stub.keepAlive(InstancePingPkg(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
        ))

        if logger_debug_enabled:
            logger.debug(
                'service heart beats, [%s], [%s]',
                config.agent_name,
                config.agent_instance_name,
            )


class GrpcTraceSegmentReportServiceAsync(TraceSegmentReportServiceAsync):
    def __init__(self, channel: grpc.aio.Channel):
        super().__init__()
        self.report_stub = TraceSegmentReportServiceStub(channel)

    async def report(self, generator):
        await self.report_stub.collect(generator)


class GrpcMeterReportServiceAsync(MeterReportServiceAsync):
    def __init__(self, channel: grpc.aio.Channel):
        super().__init__()
        self.report_stub = MeterReportServiceStub(channel)

    async def report_batch(self, generator):
        await self.report_stub.collectBatch(generator)

    async def report(self, generator):
        await self.report_stub.collect(generator)


class GrpcLogReportServiceAsync(LogDataReportServiceAsync):
    def __init__(self, channel: grpc.aio.Channel):
        super().__init__()
        self.report_stub = LogReportServiceStub(channel)

    async def report(self, generator):
        await self.report_stub.collect(generator)


class GrpcProfileTaskChannelServiceAsync(ProfileTaskChannelServiceAsync):
    def __init__(self, channel: grpc.aio.Channel):
        self.profile_stub = ProfileTaskStub(channel)

    async def do_query(self):
        query = ProfileTaskCommandQuery(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            lastCommandTime=profile_task_execution_service.get_last_command_create_time()
        )

        commands = await self.profile_stub.getProfileTaskCommands(query)
        command_service_async.receive_command(commands)  # put_nowait() not need to be awaited

    async def report(self, generator):
        await self.profile_stub.collectSnapshot(generator)

    async def finish(self, task: ProfileTask):
        finish_report = ProfileTaskFinishReport(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            taskId=task.task_id
        )
        await self.profile_stub.reportTaskFinish(finish_report)

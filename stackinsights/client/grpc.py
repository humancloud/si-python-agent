#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import grpc

from stackinsights import config
from stackinsights.client import ServiceManagementClient, TraceSegmentReportService, ProfileTaskChannelService, \
    LogDataReportService, MeterReportService
from stackinsights.command import command_service
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


class GrpcServiceManagementClient(ServiceManagementClient):
    def __init__(self, channel: grpc.Channel):
        super().__init__()
        self.instance_properties = self.get_instance_properties_proto()
        self.service_stub = ManagementServiceStub(channel)

    def send_instance_props(self):
        self.service_stub.reportInstanceProperties(InstanceProperties(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            properties=self.instance_properties,
        ))

    def send_heart_beat(self):
        self.refresh_instance_props()

        self.service_stub.keepAlive(InstancePingPkg(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
        ))

        if logger_debug_enabled:
            logger.debug(
                'service heart beats, [%s], [%s]',
                config.agent_name,
                config.agent_instance_name,
            )


class GrpcTraceSegmentReportService(TraceSegmentReportService):
    def __init__(self, channel: grpc.Channel):
        self.report_stub = TraceSegmentReportServiceStub(channel)

    def report(self, generator):
        self.report_stub.collect(generator)


class GrpcMeterReportService(MeterReportService):
    def __init__(self, channel: grpc.Channel):
        self.report_stub = MeterReportServiceStub(channel)

    def report_batch(self, generator):
        self.report_stub.collectBatch(generator)

    def report(self, generator):
        self.report_stub.collect(generator)


class GrpcLogDataReportService(LogDataReportService):
    def __init__(self, channel: grpc.Channel):
        self.report_stub = LogReportServiceStub(channel)

    def report(self, generator):
        self.report_stub.collect(generator)


class GrpcProfileTaskChannelService(ProfileTaskChannelService):
    def __init__(self, channel: grpc.Channel):
        self.profile_stub = ProfileTaskStub(channel)

    def do_query(self):
        query = ProfileTaskCommandQuery(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            lastCommandTime=profile_task_execution_service.get_last_command_create_time()
        )

        commands = self.profile_stub.getProfileTaskCommands(query)
        command_service.receive_command(commands)

    def report(self, generator):
        self.profile_stub.collectSnapshot(generator)

    def finish(self, task: ProfileTask):
        finish_report = ProfileTaskFinishReport(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            taskId=task.task_id
        )
        self.profile_stub.reportTaskFinish(finish_report)

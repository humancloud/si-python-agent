#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import json
import requests
from google.protobuf import json_format

from stackinsights import config
from stackinsights.client import ServiceManagementClient, TraceSegmentReportService, LogDataReportService
from stackinsights.loggings import logger, logger_debug_enabled


class HttpServiceManagementClient(ServiceManagementClient):
    def __init__(self):
        super().__init__()
        self.instance_properties = self.get_instance_properties()

        proto = 'https://' if config.agent_force_tls else 'http://'
        self.url_instance_props = f"{proto}{config.agent_collector_backend_services.rstrip('/')}/v3/management/reportProperties"
        self.url_heart_beat = f"{proto}{config.agent_collector_backend_services.rstrip('/')}/v3/management/keepAlive"
        self.session = requests.Session()

    def send_instance_props(self):
        res = self.session.post(self.url_instance_props, json={
            'service': config.agent_name,
            'serviceInstance': config.agent_instance_name,
            'properties': self.instance_properties,
        })
        if logger_debug_enabled:
            logger.debug('heartbeat response: %s', res)

    def send_heart_beat(self):
        self.refresh_instance_props()

        if logger_debug_enabled:
            logger.debug(
                'service heart beats, [%s], [%s]',
                config.agent_name,
                config.agent_instance_name,
            )
        res = self.session.post(self.url_heart_beat, json={
            'service': config.agent_name,
            'serviceInstance': config.agent_instance_name,
        })
        if logger_debug_enabled:
            logger.debug('heartbeat response: %s', res)


class HttpTraceSegmentReportService(TraceSegmentReportService):
    def __init__(self):
        proto = 'https://' if config.agent_force_tls else 'http://'
        self.url_report = f"{proto}{config.agent_collector_backend_services.rstrip('/')}/v3/segment"
        self.session = requests.Session()

    def report(self, generator):
        for segment in generator:
            res = self.session.post(self.url_report, json={
                'traceId': str(segment.related_traces[0]),
                'traceSegmentId': str(segment.segment_id),
                'service': config.agent_name,
                'serviceInstance': config.agent_instance_name,
                'spans': [{
                    'spanId': span.sid,
                    'parentSpanId': span.pid,
                    'startTime': span.start_time,
                    'endTime': span.end_time,
                    'operationName': span.op,
                    'peer': span.peer,
                    'spanType': span.kind.name,
                    'spanLayer': span.layer.name,
                    'componentId': span.component.value,
                    'isError': span.error_occurred,
                    'logs': [{
                        'time': int(log.timestamp * 1000),
                        'data': [{
                            'key': item.key,
                            'value': item.val,
                        } for item in log.items],
                    } for log in span.logs],
                    'tags': [{
                        'key': tag.key,
                        'value': tag.val,
                    } for tag in span.iter_tags()],
                    'refs': [{
                        'refType': 0,
                        'traceId': ref.trace_id,
                        'parentTraceSegmentId': ref.segment_id,
                        'parentSpanId': ref.span_id,
                        'parentService': ref.service,
                        'parentServiceInstance': ref.service_instance,
                        'parentEndpoint': ref.endpoint,
                        'networkAddressUsedAtPeer': ref.client_address,
                    } for ref in span.refs if ref.trace_id]
                } for span in segment.spans]
            })
            if logger_debug_enabled:
                logger.debug('report traces response: %s', res)


class HttpLogDataReportService(LogDataReportService):
    def __init__(self):
        proto = 'https://' if config.agent_force_tls else 'http://'
        self.url_report = f"{proto}{config.agent_collector_backend_services.rstrip('/')}/v3/logs"
        self.session = requests.Session()

    def report(self, generator):
        log_batch = [json.loads(json_format.MessageToJson(log_data)) for log_data in generator]
        if log_batch:  # prevent empty batches
            res = self.session.post(self.url_report, json=log_batch)
            if logger_debug_enabled:
                logger.debug('report batch log response: %s', res)

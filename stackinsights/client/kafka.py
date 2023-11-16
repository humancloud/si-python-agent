#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import ast
import os

from kafka import KafkaProducer

from stackinsights import config
from stackinsights.client import MeterReportService, ServiceManagementClient, TraceSegmentReportService, LogDataReportService
from stackinsights.loggings import logger, logger_debug_enabled
from stackinsights.protocol.language_agent.Meter_pb2 import MeterDataCollection
from stackinsights.protocol.management.Management_pb2 import InstancePingPkg, InstanceProperties

kafka_configs = {}


def __init_kafka_configs():
    kafka_configs['bootstrap_servers'] = config.kafka_bootstrap_servers.split(',')
    # process all kafka configs in env
    kafka_keys = [key for key in os.environ.keys() if key.startswith('SW_KAFKA_REPORTER_CONFIG_')]
    for kafka_key in kafka_keys:
        key = kafka_key[25:]
        val = os.environ.get(kafka_key)

        if val is not None:
            if val.isnumeric():
                val = int(val)
            elif val in ['True', 'False']:
                val = ast.literal_eval(val)
        else:
            continue

        # check if the key was already set
        if kafka_configs.get(key) is None:
            kafka_configs[key] = val
        else:
            raise KafkaConfigDuplicated(key)


__init_kafka_configs()


class KafkaServiceManagementClient(ServiceManagementClient):
    def __init__(self):
        super().__init__()
        self.instance_properties = self.get_instance_properties_proto()

        if logger_debug_enabled:
            logger.debug('kafka reporter configs: %s', kafka_configs)
        self.producer = KafkaProducer(**kafka_configs)
        self.topic_key_register = 'register-'
        self.topic = config.kafka_topic_management

        self.send_instance_props()

    def send_instance_props(self):
        instance = InstanceProperties(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
            properties=self.instance_properties,
        )

        key = bytes(self.topic_key_register + instance.serviceInstance, encoding='utf-8')
        value = instance.SerializeToString()
        self.producer.send(topic=self.topic, key=key, value=value)

    def send_heart_beat(self):
        self.refresh_instance_props()

        if logger_debug_enabled:
            logger.debug(
                'service heart beats, [%s], [%s]',
                config.agent_name,
                config.agent_instance_name,
            )

        instance_ping_pkg = InstancePingPkg(
            service=config.agent_name,
            serviceInstance=config.agent_instance_name,
        )

        key = bytes(instance_ping_pkg.serviceInstance, encoding='utf-8')
        value = instance_ping_pkg.SerializeToString()
        future = self.producer.send(topic=self.topic, key=key, value=value)
        res = future.get(timeout=10)
        if logger_debug_enabled:
            logger.debug('heartbeat response: %s', res)


class KafkaTraceSegmentReportService(TraceSegmentReportService):
    def __init__(self):
        self.producer = KafkaProducer(**kafka_configs)
        self.topic = config.kafka_topic_segment

    def report(self, generator):
        for segment in generator:
            key = bytes(segment.traceSegmentId, encoding='utf-8')
            value = segment.SerializeToString()
            self.producer.send(topic=self.topic, key=key, value=value)


class KafkaLogDataReportService(LogDataReportService):
    def __init__(self):
        self.producer = KafkaProducer(**kafka_configs)
        self.topic = config.kafka_topic_log

    def report(self, generator):
        for log_data in generator:
            key = bytes(log_data.traceContext.traceSegmentId, encoding='utf-8')
            value = log_data.SerializeToString()
            self.producer.send(topic=self.topic, key=key, value=value)


class KafkaMeterDataReportService(MeterReportService):
    def __init__(self):
        self.producer = KafkaProducer(**kafka_configs)
        self.topic = config.kafka_topic_meter

    def report(self, generator):
        collection = MeterDataCollection()
        collection.meterData.extend(list(generator))
        key = bytes(config.agent_instance_name, encoding='utf-8')
        value = collection.SerializeToString()
        self.producer.send(topic=self.topic, key=key, value=value)


class KafkaConfigDuplicated(Exception):
    def __init__(self, key):
        self.key = key

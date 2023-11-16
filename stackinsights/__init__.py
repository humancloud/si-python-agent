#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time
from collections import namedtuple
from enum import Enum
from typing import List


class Component(Enum):
    Unknown = 0
    General = 7000  # built-in modules that may not have a logo to display
    Flask = 7001
    Requests = 7002
    PyMysql = 7003
    Django = 7004
    Tornado = 7005
    Redis = 7
    MongoDB = 9
    PostgreSQL = 22
    KafkaProducer = 40
    KafkaConsumer = 41
    RabbitmqProducer = 52
    RabbitmqConsumer = 53
    Elasticsearch = 47
    HBase = 94
    Neo4j = 112
    Urllib3 = 7006
    Sanic = 7007
    AioHttp = 7008
    Pyramid = 7009
    Psycopg = 7010
    Celery = 7011
    Falcon = 7012
    MysqlClient = 7013
    FastAPI = 7014
    Bottle = 7015
    AsyncPG = 7016
    AIORedis = 7017
    Websockets = 7018
    HTTPX = 7019


class Layer(Enum):
    Unknown = 0
    Database = 1
    RPCFramework = 2
    Http = 3
    MQ = 4
    Cache = 5


class Kind(Enum):
    Local = 0
    Entry = 1
    Exit = 2

    @property
    def is_local(self):
        return self == Kind.Local

    @property
    def is_entry(self):
        return self == Kind.Entry

    @property
    def is_exit(self):
        return self == Kind.Exit


LogItem = namedtuple('LogItem', 'key val')


class Log(object):

    def __init__(self, timestamp: time = time.time(), items: List[LogItem] = None): # noqa
        self.timestamp = timestamp
        self.items = items or []
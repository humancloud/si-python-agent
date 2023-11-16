#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

class Tag:
    key: str = ''
    overridable: bool = True

    def __init__(self, val):
        try:
            self.val = str(val)
        except ValueError:
            raise ValueError('Tag value must be a string or convertible to a string')


class TagHttpMethod(Tag):
    key = 'http.method'


class TagHttpURL(Tag):
    key = 'http.url'


class TagHttpStatusCode(Tag):
    key = 'http.status_code'


class TagHttpStatusMsg(Tag):
    key = 'http.status_msg'


class TagHttpParams(Tag):
    key = 'http.params'


class TagDbType(Tag):
    key = 'db.type'


class TagDbInstance(Tag):
    key = 'db.instance'


class TagDbStatement(Tag):
    key = 'db.statement'


class TagDbSqlParameters(Tag):
    key = 'db.sql.parameters'
    overridable = False


class TagCacheType(Tag):
    key = 'cache.type'


class TagCacheOp(Tag):
    key = 'cache.op'


class TagCacheCmd(Tag):
    key = 'cache.cmd'


class TagCacheKey(Tag):
    key = 'cache.key'


class TagMqBroker(Tag):
    key = 'mq.broker'


class TagMqTopic(Tag):
    key = 'mq.topic'


class TagMqQueue(Tag):
    key = 'mq.queue'


class TagCeleryParameters(Tag):
    key = 'celery.parameters'

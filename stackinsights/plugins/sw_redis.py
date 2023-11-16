#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagCacheType, TagCacheOp, TagCacheCmd, TagCacheKey

link_vector = ['https://github.com/andymccurdy/redis-py/']
support_matrix = {
    'redis': {
        '>=3.7': ['3.5.*', '4.5.1']
    }
}
note = """"""

OPERATIONS_WRITE = {'GETSET', 'SET', 'SETBIT', 'SETEX ', 'SETNX ', 'SETRANGE', 'STRLEN ', 'MSET', 'MSETNX ', 'PSETEX',
                    'INCR ', 'INCRBY ', 'INCRBYFLOAT', 'DECR ', 'DECRBY ', 'APPEND ', 'HMSET', 'HSET', 'HSETNX ',
                    'HINCRBY', 'HINCRBYFLOAT', 'HDEL', 'RPOPLPUSH', 'RPUSH', 'RPUSHX', 'LPUSH', 'LPUSHX', 'LREM',
                    'LTRIM', 'LSET', 'BRPOPLPUSH', 'LINSERT', 'SADD', 'SDIFF', 'SDIFFSTORE', 'SINTERSTORE', 'SISMEMBER',
                    'SREM', 'SUNION', 'SUNIONSTORE', 'SINTER', 'ZADD', 'ZINCRBY', 'ZINTERSTORE', 'ZRANGE',
                    'ZRANGEBYLEX', 'ZRANGEBYSCORE', 'ZRANK', 'ZREM', 'ZREMRANGEBYLEX', 'ZREMRANGEBYRANK',
                    'ZREMRANGEBYSCORE', 'ZREVRANGE', 'ZREVRANGEBYSCORE', 'ZREVRANK', 'ZUNIONSTORE', 'XADD', 'XDEL',
                    'DEL', 'XTRIM'}

OPERATIONS_READ = {'GETRANGE', 'GETBIT ', 'MGET', 'HVALS', 'HKEYS', 'HLEN', 'HEXISTS', 'HGET', 'HGETALL', 'HMGET',
                   'BLPOP', 'BRPOP', 'LINDEX', 'LLEN', 'LPOP', 'LRANGE', 'RPOP', 'SCARD', 'SRANDMEMBER', 'SPOP',
                   'SSCAN', 'SMOVE', 'ZLEXCOUNT', 'ZSCORE', 'ZSCAN', 'ZCARD', 'ZCOUNT', 'XGET', 'GET', 'XREAD', 'XLEN',
                   'XRANGE', 'XREVRANGE'}


def install():
    from redis.connection import Connection

    _send_command = Connection.send_command

    def _sw_send_command(this: Connection, *args, **kwargs):
        peer = f'{this.host}:{this.port}'

        if len(args) == 1:
            cmd = args[0]
            key = ''
        elif len(args) > 1:
            cmd, key = args[0], args[1]
        else:  # just to be safe
            cmd = key = ''

        if cmd in OPERATIONS_WRITE:
            op = 'write'
        elif cmd in OPERATIONS_READ:
            op = 'read'
        else:
            op = ''

        context = get_context()
        with context.new_exit_span(op=f'Redis/{cmd}' or '/', peer=peer, component=Component.Redis) as span:
            span.layer = Layer.Cache

            res = _send_command(this, *args, **kwargs)
            span.tag(TagCacheType('Redis'))
            span.tag(TagCacheKey(key))
            span.tag(TagCacheCmd(cmd))
            span.tag(TagCacheOp(op))

            return res

    Connection.send_command = _sw_send_command

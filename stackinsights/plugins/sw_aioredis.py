#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagDbType, TagDbInstance, TagDbStatement

link_vector = ['https://aioredis.readthedocs.io/']
support_matrix = {
    'aioredis': {
        '>=3.7': ['2.0.*']
    }
}
note = """"""


def install():
    from aioredis import Redis

    async def _sw_execute_command(self, op, *args, **kwargs):
        connargs = self.connection_pool.connection_kwargs
        peer = f'{connargs.get("host", "localhost")}:{connargs.get("port", 6379)}'

        context = get_context()
        with context.new_exit_span(op=f'Redis/AIORedis/{op}' or '/', peer=peer, component=Component.AIORedis) as span:
            span.layer = Layer.Cache

            span.tag(TagDbType('Redis'))
            span.tag(TagDbInstance(str(connargs.get('db', 0))))
            span.tag(TagDbStatement(op))

            return await _execute_command(self, op, *args, **kwargs)

    _execute_command = Redis.execute_command
    Redis.execute_command = _sw_execute_command


# Example code for someone who might want to make tests:
#
# async def aioredis_():
#     redis = aioredis.from_url("redis://localhost")
#     await redis.set("my-key", "value")
#     value = await redis.get("my-key")
#     print(value)

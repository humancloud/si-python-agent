#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagMqBroker, TagMqTopic, TagMqQueue

link_vector = ['https://pypi.org/project/aiormq/']
support_matrix = {
    'aiormq': {
        '>=3.7': ['6.3', '6.4']
    }
}
note = """"""


def install():
    from aiormq import Channel
    from aiormq.tools import awaitable

    try:
        from pamqp import commands as spec  # aiormq v6.4.1
    except ImportError:
        from pamqp import specification as spec  # aiormq v3.3.1

    async def _sw_basic_publish(self, body, exchange='', routing_key='', properties=None, **kwargs):
        url = self.connection.url
        peer = f'{url.host}:{url.port}' if url.port else url.host
        context = get_context()

        with context.new_exit_span(op=f'RabbitMQ/Topic/{exchange}/Queue/{routing_key}/Producer',
                                   peer=peer, component=Component.RabbitmqProducer) as span:
            span.tag(TagMqBroker(peer))
            span.tag(TagMqTopic(exchange))
            span.tag(TagMqQueue(routing_key))

            span.layer = Layer.MQ
            carrier = span.inject()

            if properties is None:
                properties = spec.Basic.Properties(delivery_mode=1)

            headers = getattr(properties, 'headers', None)

            if headers is None:
                headers = properties.headers = {}

            for item in carrier:
                headers[item.key] = item.val

            return await _basic_publish(self, body, exchange=exchange, routing_key=routing_key, properties=properties, **kwargs)

    async def _sw_basic_consume(self, queue, consumer_callback, *args, **kwargs):
        async def _callback(msg):
            context = get_context()
            url = self.connection.url
            peer = f'{url.host}:{url.port}' if url.port else url.host
            exchange = msg.delivery.exchange
            routing_key = msg.delivery.routing_key
            headers = msg.header.properties.headers
            carrier = Carrier()

            for item in carrier:
                if item.key in headers:
                    val = headers.get(item.key)
                    if val is not None:
                        item.val = val if isinstance(val, str) else val.decode()

            with context.new_entry_span(op='RabbitMQ/Topic/' + exchange + '/Queue/' + routing_key
                                        + '/Consumer' or '', carrier=carrier) as span:
                span.layer = Layer.MQ
                span.component = Component.RabbitmqConsumer
                span.tag(TagMqBroker(peer))
                span.tag(TagMqTopic(exchange))
                span.tag(TagMqQueue(routing_key))

                return await awaitable(consumer_callback)(msg)

        return await _basic_consume(self, queue, _callback, *args, **kwargs)

    _basic_publish = Channel.basic_publish
    _basic_consume = Channel.basic_consume
    Channel.basic_publish = _sw_basic_publish
    Channel.basic_consume = _sw_basic_consume

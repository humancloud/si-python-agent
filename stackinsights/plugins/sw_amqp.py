#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagMqBroker, TagMqTopic, TagMqQueue

link_vector = ['https://pypi.org/project/amqp/']
support_matrix = {
    'amqp': {
        '>=3.7': ['2.6.1']
    }
}
note = """"""


def install():
    from amqp import Channel

    def _sw_basic_publish(self, msg, exchange='', routing_key='', *args, **kwargs):
        peer = getattr(self.connection, 'host', '<unavailable>')

        with get_context().new_exit_span(op=f'RabbitMQ/Topic/{exchange}/Queue/{routing_key}/Producer',
                                         peer=peer, component=Component.RabbitmqProducer) as span:
            span.tag(TagMqBroker(peer))
            span.tag(TagMqTopic(exchange))
            span.tag(TagMqQueue(routing_key))

            span.layer = Layer.MQ
            carrier = span.inject()
            headers = getattr(msg, 'headers', None)

            if headers is None:
                headers = msg.headers = {}

            for item in carrier:
                headers[item.key] = item.val

            return _basic_publish(self, msg, exchange, routing_key, *args, **kwargs)

    def _sw_basic_consume(self, queue='', consumer_tag='', no_local=False,
                          no_ack=False, exclusive=False, nowait=False,
                          callback=None, arguments=None, on_cancel=None,
                          argsig='BssbbbbF'):
        def _callback(msg):
            peer = getattr(self.connection, 'host', '<unavailable>')
            delivery_info = getattr(msg, 'delivery_info', {})
            exchange = delivery_info.get('exchange', '<unavailable>')
            routing_key = delivery_info.get('routing_key', '<unavailable>')
            headers = getattr(msg, 'headers', {})
            carrier = Carrier()

            for item in carrier:
                if item.key in headers:
                    val = headers.get(item.key)
                    if val is not None:
                        item.val = val

            with get_context().new_entry_span(op='RabbitMQ/Topic/' + exchange + '/Queue/' + routing_key
                                              + '/Consumer' or '', carrier=carrier) as span:
                span.layer = Layer.MQ
                span.component = Component.RabbitmqConsumer
                span.tag(TagMqBroker(peer))
                span.tag(TagMqTopic(exchange))
                span.tag(TagMqQueue(routing_key))

                return callback(msg)

        return _basic_consume(self, queue=queue, consumer_tag=consumer_tag, no_local=no_local, no_ack=no_ack,
                              exclusive=exclusive, nowait=nowait, callback=_callback, arguments=arguments,
                              on_cancel=on_cancel, argsig=argsig)

    _basic_publish = Channel.basic_publish
    _basic_consume = Channel.basic_consume
    Channel.basic_publish = Channel._basic_publish = _sw_basic_publish
    Channel.basic_consume = _sw_basic_consume

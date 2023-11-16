#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagDbType, TagDbStatement

link_vector = ['https://github.com/elastic/elasticsearch-py']
support_matrix = {
    'elasticsearch': {
        '>=3.7': ['7.13', '7.14', '7.15'],
    }
}
note = """"""


def install():
    from elasticsearch import Transport
    _perform_request = Transport.perform_request

    def _sw_perform_request(this: Transport, method, url, headers=None, params=None, body=None):
        context = get_context()
        peer = ','.join([f"{host['host']}:{str(host['port'])}" for host in this.hosts])
        with context.new_exit_span(op=f'Elasticsearch/{method}{url}', peer=peer,
                                   component=Component.Elasticsearch) as span:
            span.layer = Layer.Database
            res = _perform_request(this, method, url, headers=headers, params=params, body=body)

            span.tag(TagDbType('Elasticsearch'))
            if config.plugin_elasticsearch_trace_dsl:
                span.tag(TagDbStatement('' if body is None else body))

            return res

    Transport.perform_request = _sw_perform_request

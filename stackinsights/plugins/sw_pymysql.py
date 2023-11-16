#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagDbType, TagDbInstance, TagDbStatement, TagDbSqlParameters

link_vector = ['https://pymysql.readthedocs.io/en/latest/']
support_matrix = {
    'pymysql': {
        '>=3.7': ['1.0']
    }
}
note = """"""


def install():
    from pymysql.cursors import Cursor

    _execute = Cursor.execute

    def _sw_execute(this: Cursor, query, args=None):
        peer = f'{this.connection.host}:{this.connection.port}'

        context = get_context()
        with context.new_exit_span(op='Mysql/PyMsql/execute', peer=peer, component=Component.PyMysql) as span:
            span.layer = Layer.Database
            res = _execute(this, query, args)

            span.tag(TagDbType('mysql'))
            span.tag(TagDbInstance((this.connection.db or b'').decode('utf-8')))
            span.tag(TagDbStatement(query))

            if config.plugin_sql_parameters_max_length and args:
                parameter = ','.join([str(arg) for arg in args])
                max_len = config.plugin_sql_parameters_max_length
                parameter = f'{parameter[0:max_len]}...' if len(parameter) > max_len else parameter
                span.tag(TagDbSqlParameters(f'[{parameter}]'))

            return res

    Cursor.execute = _sw_execute

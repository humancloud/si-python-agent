#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagDbType, TagDbInstance, TagDbStatement, TagDbSqlParameters

link_vector = ['https://mysqlclient.readthedocs.io/']
support_matrix = {
    'mysqlclient': {
        '>=3.7': ['2.1.*']
    }
}
note = """"""


def install():
    import wrapt
    import MySQLdb

    _connect = MySQLdb.connect

    def _sw_connect(*args, **kwargs):
        con = _connect(*args, **kwargs)
        con.host = kwargs['host']
        if 'db' in kwargs:
            con.db = kwargs['db']
        else:
            con.db = kwargs['database']
        return ProxyConnection(con)

    class ProxyCursor(wrapt.ObjectProxy):
        def __init__(self, cur):
            wrapt.ObjectProxy.__init__(self, cur)

            self._self_cur = cur

        def __enter__(self):
            return ProxyCursor(wrapt.ObjectProxy.__enter__(self))

        def execute(self, query, args=None):
            peer = f'{self.connection.host}:{self.connection.port}'
            with get_context().new_exit_span(op='Mysql/MysqlClient/execute', peer=peer,
                                             component=Component.MysqlClient) as span:
                span.layer = Layer.Database
                span.tag(TagDbType('mysql'))
                span.tag(TagDbInstance((self.connection.db or '')))
                span.tag(TagDbStatement(query))

                if config.plugin_sql_parameters_max_length and args:
                    parameter = ','.join([str(arg) for arg in args])
                    max_len = config.plugin_sql_parameters_max_length
                    parameter = f'{parameter[0:max_len]}...' if len(parameter) > max_len else parameter
                    span.tag(TagDbSqlParameters(f'[{parameter}]'))

                return self._self_cur.execute(query, args)

    class ProxyConnection(wrapt.ObjectProxy):
        def __init__(self, conn):
            wrapt.ObjectProxy.__init__(self, conn)

            self._self_conn = conn

        def __enter__(self):
            return ProxyConnection(wrapt.ObjectProxy.__enter__(self))

        def cursor(self, cursorclass=None):
            return ProxyCursor(self._self_conn.cursor(cursorclass))

    MySQLdb.connect = _sw_connect

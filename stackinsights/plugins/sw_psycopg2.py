#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import TagDbType, TagDbInstance, TagDbStatement, TagDbSqlParameters

link_vector = ['https://www.psycopg.org/']
support_matrix = {
    'psycopg2-binary': {
        '>=3.10': [],
        '>=3.7': ['2.9']  # transition to psycopg(3), not working for python 3.10
    }
}
note = """"""


def install():
    import wrapt  # psycopg2 is read-only C extension objects so they need to be proxied
    import psycopg2

    class ProxyCursor(wrapt.ObjectProxy):
        def __init__(self, cur):
            wrapt.ObjectProxy.__init__(self, cur)

            self._self_cur = cur

        def __enter__(self):
            return ProxyCursor(wrapt.ObjectProxy.__enter__(self))

        def execute(self, query, vars=None):
            dsn = self.connection.get_dsn_parameters()
            peer = f"{dsn['host']}:{dsn['port']}"

            with get_context().new_exit_span(op='PostgreSQL/Psycopg/execute', peer=peer,
                                             component=Component.Psycopg) as span:
                span.layer = Layer.Database

                span.tag(TagDbType('PostgreSQL'))
                span.tag(TagDbInstance(dsn['dbname']))
                span.tag(TagDbStatement(query))

                if config.plugin_sql_parameters_max_length and vars is not None:
                    text = ','.join(str(v) for v in vars)

                    if len(text) > config.plugin_sql_parameters_max_length:
                        text = f'{text[:config.plugin_sql_parameters_max_length]}...'

                    span.tag(TagDbSqlParameters(f'[{text}]'))

                return self._self_cur.execute(query, vars)

        def executemany(self, query, vars_list):
            dsn = self.connection.get_dsn_parameters()
            peer = f"{dsn['host']}:{dsn['port']}"

            with get_context().new_exit_span(op='PostgreSQL/Psycopg/executemany', peer=peer,
                                             component=Component.Psycopg) as span:
                span.layer = Layer.Database

                span.tag(TagDbType('PostgreSQL'))
                span.tag(TagDbInstance(dsn['dbname']))
                span.tag(TagDbStatement(query))

                if config.plugin_sql_parameters_max_length:
                    max_len = config.plugin_sql_parameters_max_length
                    total_len = 0
                    text_list = []

                    for vars in vars_list:
                        text = f"[{','.join(str(v) for v in vars)}]"
                        total_len += len(text)

                        if total_len > max_len:
                            text_list.append(f'{text[:max_len - total_len]}...')

                            break

                        text_list.append(text)

                    span.tag(TagDbSqlParameters(f"[{','.join(text_list)}]"))

                return self._self_cur.executemany(query, vars_list)

        def callproc(self, procname, parameters=None):
            dsn = self.connection.get_dsn_parameters()
            peer = f"{dsn['host']}:{dsn['port']}"

            with get_context().new_exit_span(op='PostgreSQL/Psycopg/callproc', peer=peer,
                                             component=Component.Psycopg) as span:
                span.layer = Layer.Database
                args = f"({'' if not parameters else ','.join(parameters)})"

                span.tag(TagDbType('PostgreSQL'))
                span.tag(TagDbInstance(dsn['dbname']))
                span.tag(TagDbStatement(procname + args))

                return self._self_cur.callproc(procname, parameters)

    class ProxyConnection(wrapt.ObjectProxy):
        def __init__(self, conn):
            wrapt.ObjectProxy.__init__(self, conn)

            self._self_conn = conn

        def __enter__(self):
            return ProxyConnection(wrapt.ObjectProxy.__enter__(self))

        def cursor(self, *args, **kwargs):
            return ProxyCursor(self._self_conn.cursor(*args, **kwargs))

    def connect(*args, **kwargs):
        return ProxyConnection(_connect(*args, **kwargs))

    _connect = psycopg2.connect
    psycopg2.connect = connect

    try:  # try to instrument register_type which will fail if it gets a wrapped cursor or connection
        from psycopg2._psycopg import register_type as _register_type

        def register_type(c, conn_or_curs=None):
            if isinstance(conn_or_curs, ProxyConnection):
                conn_or_curs = conn_or_curs._self_conn
            elif isinstance(conn_or_curs, ProxyCursor):
                conn_or_curs = conn_or_curs._self_cur

            return _register_type(c, conn_or_curs)

        try:
            import psycopg2._ipaddress

            if psycopg2._ipaddress.register_type is _register_type:
                psycopg2._ipaddress.register_type = register_type

        except Exception:
            pass

        try:
            import psycopg2._ipaddress

            if psycopg2._json.register_type is _register_type:
                psycopg2._json.register_type = register_type

        except Exception:
            pass

        try:
            import psycopg2._ipaddress

            if psycopg2._range.register_type is _register_type:
                psycopg2._range.register_type = register_type

        except Exception:
            pass

        try:
            import psycopg2._ipaddress

            if psycopg2.extensions.register_type is _register_type:
                psycopg2.extensions.register_type = register_type

        except Exception:
            pass

    except Exception:
        pass

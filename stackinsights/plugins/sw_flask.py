#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode, TagHttpParams

link_vector = ['https://flask.palletsprojects.com']
support_matrix = {
    'flask': {
        '>=3.7': ['2.0']  # 1.x removed due to EOL
    }
}
note = """"""


def install():
    from flask import Flask
    _full_dispatch_request = Flask.full_dispatch_request
    _handle_user_exception = Flask.handle_user_exception
    _handle_exception = Flask.handle_exception

    def params_tostring(params):
        return '\n'.join([f"{k}=[{','.join(params.getlist(k))}]" for k, _ in params.items()])

    def _sw_full_dispatch_request(this: Flask):
        import flask

        req = flask.request
        carrier = Carrier()
        method = req.method

        for item in carrier:
            if item.key.capitalize() in req.headers:
                item.val = req.headers[item.key.capitalize()]

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_entry_span(op=req.path, carrier=carrier, inherit=Component.General)

        with span:
            span.layer = Layer.Http
            span.component = Component.Flask
            if all(environ_key in req.environ for environ_key in ('REMOTE_ADDR', 'REMOTE_PORT')):
                span.peer = f"{req.environ['REMOTE_ADDR']}:{req.environ['REMOTE_PORT']}"
            span.tag(TagHttpMethod(method))
            span.tag(TagHttpURL(req.url.split('?')[0]))
            if config.plugin_flask_collect_http_params and req.values:
                span.tag(TagHttpParams(params_tostring(req.values)[0:config.plugin_http_http_params_length_threshold]))
            resp = _full_dispatch_request(this)

            if resp.status_code >= 400:
                span.error_occurred = True

            span.tag(TagHttpStatusCode(resp.status_code))
            return resp

    def _sw_handle_user_exception(this: Flask, e):
        if e is not None:
            entry_span = get_context().active_span
            if entry_span is not None and type(entry_span) is not NoopSpan:
                entry_span.raised()

        return _handle_user_exception(this, e)

    def _sw_handle_exception(this: Flask, e):
        if e is not None:
            entry_span = get_context().active_span
            if entry_span is not None and type(entry_span) is not NoopSpan:
                entry_span.raised()

        return _handle_exception(this, e)

    Flask.full_dispatch_request = _sw_full_dispatch_request
    Flask.handle_user_exception = _sw_handle_user_exception
    Flask.handle_exception = _sw_handle_exception

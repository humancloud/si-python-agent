#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from stackinsights import Layer, Component, config
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode, TagHttpParams

link_vector = ['https://fastapi.tiangolo.com']
support_matrix = {
    'fastapi': {
        '>=3.7': ['0.89.*', '0.88.*']
    }
}
note = """"""


def install():
    from starlette.types import Receive, Scope, Send, Message
    try:
        from starlette.middleware.exceptions import ExceptionMiddleware
    except ImportError:  # deprecated in newer versions
        from starlette.exceptions import ExceptionMiddleware
    from starlette.requests import Request
    from starlette.websockets import WebSocket  # FastAPI imports from starlette.websockets

    _original_fast_api = ExceptionMiddleware.__call__

    def params_tostring(params):
        return '\n'.join([f"{k}=[{','.join(params.getlist(k))}]" for k, _ in params.items()])

    async def create_span(self, method, scope, req, send, receive):
        carrier = Carrier()

        for item in carrier:
            if item.key.capitalize() in req.headers:
                item.val = req.headers[item.key.capitalize()]

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_entry_span(op=dict(scope)['path'], carrier=carrier, inherit=Component.General)

        with span:
            span.layer = Layer.Http
            span.component = Component.FastAPI
            span.peer = f'{req.client.host}:{req.client.port}'
            span.tag(TagHttpMethod(method))
            span.tag(TagHttpURL(str(req.url).split('?')[0]))
            if config.plugin_fastapi_collect_http_params and req.query_params:
                span.tag(TagHttpParams(params_tostring(req.query_params)[0:config.plugin_http_http_params_length_threshold]))

            status_code = 500

            async def wrapped_send(message: Message) -> None:
                nonlocal status_code

                if message['type'] == 'http.response.start':
                    status_code = message['status']

                elif message['type'] == 'websocket.accept' or message['type'] == 'websocket.close':
                    status_code = 200

                await send(message)

            try:  # return handle to original
                await _original_fast_api(self, scope, receive, wrapped_send)
            finally:
                span.tag(TagHttpStatusCode(status_code))
                if status_code >= 400:
                    span.error_occurred = True

    async def _sw_fast_api(self, scope: Scope, receive: Receive, send: Send):

        if scope['type'] == 'websocket':
            ws = WebSocket(scope, receive=receive, send=send)
            method = 'websocket.accept'
            await create_span(self, method, scope, ws, send, receive)

        elif scope['type'] == 'http':
            req = Request(scope, receive=receive, send=send)
            method = req.method
            await create_span(self, method, scope, req, send, receive)

        else:
            await _original_fast_api(self, scope, receive, send)

    ExceptionMiddleware.__call__ = _sw_fast_api

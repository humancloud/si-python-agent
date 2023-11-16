#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpParams, TagHttpStatusCode, TagHttpStatusMsg

link_vector = ['https://falcon.readthedocs.io/en/stable/']
support_matrix = {
    'hug': {
        '>=3.11': [],
        '>=3.10': ['2.5', '2.6'],  # api deprecated for 3.10
        '>=3.7': ['2.4.1', '2.5', '2.6'],  # support begins 2.4.1
    }
}
note = """While Falcon is instrumented, only Hug is tested.
Hug is believed to be abandoned project, use this plugin with a bit more caution.
Instead of Hug, plugin test should move to test actual Falcon."""


def install():
    from falcon import API, request, RequestOptions

    _original_falcon_api = API.__call__

    def _sw_falcon_api(this: API, env, start_response):
        context = get_context()
        carrier = Carrier()
        req = request.Request(env, RequestOptions())
        headers = req.headers
        method = req.method

        for item in carrier:
            key = item.key.upper()
            if key in headers:
                item.val = headers[key]

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else context.new_entry_span(op=req.path, carrier=carrier)

        with span:
            span.layer = Layer.Http
            span.component = Component.Falcon
            span.peer = req.remote_addr

            span.tag(TagHttpMethod(method))
            span.tag(TagHttpURL(str(req.url)))

            if req.params:
                span.tag(TagHttpParams(','.join([f'{k}={v}' for k, v in req.params.items()])))

            def _start_response(resp_status, headers):
                try:
                    code, msg = resp_status.split(' ', 1)
                    code = int(code)
                except Exception:
                    code, msg = 500, 'Internal Server Error'

                if code >= 400:
                    span.error_occurred = True

                span.tag(TagHttpStatusCode(code))
                span.tag(TagHttpStatusMsg(msg))

                return start_response(resp_status, headers)

            try:
                return _original_falcon_api(this, env, _start_response)

            except Exception:
                span.raised()

                raise

    API.__call__ = _sw_falcon_api

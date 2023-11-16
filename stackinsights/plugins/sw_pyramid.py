#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode

link_vector = ['https://trypyramid.com']
support_matrix = {
    'pyramid': {
        '>=3.7': ['1.10', '2.0']
    }
}
note = """"""


def install():
    from pyramid.router import Router

    def _sw_invoke_request(self, request, *args, **kwargs):
        carrier = Carrier()
        method = request.method

        for item in carrier:
            val = request.headers.get(item.key)

            if val is not None:
                item.val = val

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_entry_span(op=request.path, carrier=carrier)

        with span:
            span.layer = Layer.Http
            span.component = Component.Pyramid
            span.peer = request.remote_host or request.remote_addr

            span.tag(TagHttpMethod(method))
            span.tag(TagHttpURL(str(request.url)))

            resp = _invoke_request(self, request, *args, **kwargs)

            span.tag(TagHttpStatusCode(resp.status_code))

            if resp.status_code >= 400:
                span.error_occurred = True

        return resp

    _invoke_request = Router.invoke_request
    Router.invoke_request = _sw_invoke_request

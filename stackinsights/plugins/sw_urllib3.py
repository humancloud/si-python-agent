#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode

link_vector = ['https://urllib3.readthedocs.io/en/latest/']
support_matrix = {
    'urllib3': {
        '>=3.7': ['1.26', '1.25']
    }
}
note = """"""


def install():
    from urllib3.request import RequestMethods

    _request = RequestMethods.request

    def _sw_request(this: RequestMethods, method, url, fields=None, headers=None, **urlopen_kw):
        from stackinsights.utils.filter import sw_urlparse

        url_param = sw_urlparse(url)

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_exit_span(op=url_param.path or '/', peer=url_param.netloc,
                                             component=Component.Urllib3)

        with span:
            carrier = span.inject()
            span.layer = Layer.Http

            if headers is None:
                headers = {}
            for item in carrier:
                headers[item.key] = item.val

            span.tag(TagHttpMethod(method.upper()))
            span.tag(TagHttpURL(url_param.geturl()))

            res = _request(this, method, url, fields=fields, headers=headers, **urlopen_kw)

            span.tag(TagHttpStatusCode(res.status))
            if res.status >= 400:
                span.error_occurred = True

            return res

    RequestMethods.request = _sw_request

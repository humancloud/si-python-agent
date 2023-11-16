#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode

link_vector = ['https://requests.readthedocs.io/en/master/']
support_matrix = {
    'requests': {
        '>=3.7': ['2.26', '2.25']
    }
}
note = """"""


def install():
    from requests import Session
    from stackinsights.utils.filter import sw_urlparse

    _request = Session.request

    def _sw_request(this: Session, method, url,
                    params=None, data=None, headers=None, cookies=None, files=None,
                    auth=None, timeout=None, allow_redirects=True, proxies=None,
                    hooks=None, stream=None, verify=None, cert=None, json=None):

        url_param = sw_urlparse(url)

        # ignore trace stackinsights self request
        if config.agent_protocol == 'http' and config.agent_collector_backend_services.rstrip('/').endswith(url_param.netloc):
            return _request(this, method, url, params, data, headers, cookies, files, auth, timeout,
                            allow_redirects,
                            proxies,
                            hooks, stream, verify, cert, json)

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_exit_span(op=url_param.path or '/', peer=url_param.netloc,
                                             component=Component.Requests)

        with span:
            carrier = span.inject()
            span.layer = Layer.Http

            if headers is None:
                headers = {}
            for item in carrier:
                headers[item.key] = item.val

            span.tag(TagHttpMethod(method.upper()))
            span.tag(TagHttpURL(url_param.geturl()))

            res = _request(this, method, url, params, data, headers, cookies, files, auth, timeout,
                           allow_redirects,
                           proxies,
                           hooks, stream, verify, cert, json)

            span.tag(TagHttpStatusCode(res.status_code))
            if res.status_code >= 400:
                span.error_occurred = True

            return res

    Session.request = _sw_request

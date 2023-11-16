#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode

link_vector = ['https://docs.aiohttp.org']
support_matrix = {
    'aiohttp': {
        '>=3.7': ['3.7.*']  # TODO: support 3.8
    }
}
note = """"""


def install():
    from aiohttp import ClientSession
    from aiohttp.web_protocol import RequestHandler
    from aiohttp.web_request import BaseRequest
    from multidict import CIMultiDict, MultiDict, MultiDictProxy
    from yarl import URL

    _request = ClientSession._request

    async def _sw_request(self: ClientSession, method: str, str_or_url, **kwargs):
        url = URL(str_or_url).with_user(None).with_password(None)
        peer = f"{url.host or ''}:{url.port or ''}"

        if config.agent_protocol == 'http' and config.agent_collector_backend_services.rstrip('/') \
                .endswith(f'{url.host}:{url.port}'):
            return _request

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_exit_span(op=url.path or '/', peer=peer, component=Component.AioHttp)

        with span:
            span.layer = Layer.Http
            span.tag(TagHttpMethod(method.upper()))  # pyre-ignore
            span.tag(TagHttpURL(str(url.with_password(None))))  # pyre-ignore

            carrier = span.inject()
            headers = kwargs.get('headers')

            if headers is None:
                headers = kwargs['headers'] = CIMultiDict()
            elif not isinstance(headers, (MultiDictProxy, MultiDict)):
                headers = CIMultiDict(headers)
                kwargs['headers'] = headers

            for item in carrier:
                headers.add(item.key, item.val)

            res = await _request(self, method, str_or_url, **kwargs)

            span.tag(TagHttpStatusCode(res.status))

            if res.status >= 400:
                span.error_occurred = True

            return res

    ClientSession._request = _sw_request

    _handle_request = RequestHandler._handle_request

    async def _sw_handle_request(self, request: BaseRequest, start_time: float):

        if config.agent_protocol == 'http' and config.agent_collector_backend_services.rstrip('/') \
                .endswith(f'{request.url.host}:{request.url.port}'):
            return _handle_request

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
            span.component = Component.AioHttp
            peer_name = request._transport_peername
            if isinstance(peer_name, (list, tuple)):
                span.peer = f'{peer_name[0]}:{peer_name[1]}'
            else:
                span.peer = f'{peer_name}'

            span.tag(TagHttpMethod(method))  # pyre-ignore
            span.tag(TagHttpURL(str(request.url)))  # pyre-ignore

            resp, reset = await _handle_request(self, request, start_time)

            span.tag(TagHttpStatusCode(resp.status))

            if resp.status >= 400:
                span.error_occurred = True

        return resp, reset

    RequestHandler._handle_request = _sw_handle_request

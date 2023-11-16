#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights import Layer, Component, config
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.context import get_context, NoopContext
from stackinsights.trace.span import NoopSpan
from stackinsights.trace.tags import TagHttpMethod, TagHttpURL, TagHttpStatusCode, TagHttpParams

link_vector = ['https://www.djangoproject.com/']
support_matrix = {
    'django': {
        '>=3.7': ['3.2'],
        # ">=3.8": ["4.0a1"]  # expected Dec 2021
    }
}
note = """"""


def install():
    from django.core.handlers.base import BaseHandler
    from django.core.handlers import exception

    _get_response = BaseHandler.get_response
    _handle_uncaught_exception = exception.handle_uncaught_exception

    def _sw_get_response(this, request):
        if request is None:
            resp = _get_response(this, request)
            return resp

        carrier = Carrier()
        method = request.method

        for item in carrier:
            # Any HTTP headers in the request are converted to META keys by converting all characters to uppercase,
            # replacing any hyphens with underscores and adding an HTTP_ prefix to the name.
            # https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpRequest.META
            sw_http_header_key = f"HTTP_{item.key.upper().replace('-', '_')}"
            if sw_http_header_key in request.META:
                item.val = request.META[sw_http_header_key]

        span = NoopSpan(NoopContext()) if config.ignore_http_method_check(method) \
            else get_context().new_entry_span(op=request.path, carrier=carrier)

        with span:
            span.layer = Layer.Http
            span.component = Component.Django
            span.peer = f"{request.META.get('REMOTE_ADDR')}:{request.META.get('REMOTE_PORT') or '80'}"

            span.tag(TagHttpMethod(method))
            span.tag(TagHttpURL(request.build_absolute_uri().split('?')[0]))

            # you can get request parameters by `request.GET` even though client are using POST or other methods
            if config.plugin_django_collect_http_params and request.GET:
                span.tag(TagHttpParams(params_tostring(request.GET)[0:config.plugin_http_http_params_length_threshold]))

            resp = _get_response(this, request)
            span.tag(TagHttpStatusCode(resp.status_code))
            if resp.status_code >= 400:
                span.error_occurred = True
            return resp

    def _sw_handle_uncaught_exception(request, resolver, exc_info):
        if exc_info is not None:
            entry_span = get_context().active_span
            if entry_span is not None:
                entry_span.raised()

        return _handle_uncaught_exception(request, resolver, exc_info)

    BaseHandler.get_response = _sw_get_response
    exception.handle_uncaught_exception = _sw_handle_uncaught_exception


def params_tostring(params):
    return '\n'.join([f"{k}=[{','.join(params.getlist(k))}]" for k, _ in params.items()])

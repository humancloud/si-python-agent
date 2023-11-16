#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from collections import namedtuple

import grpc


class _ClientInterceptorAsync(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
    grpc.aio.StreamUnaryClientInterceptor,
    grpc.aio.StreamStreamClientInterceptor
):

    def __init__(self, interceptor_async_function):
        self._fn = interceptor_async_function

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = await \
            self._fn(client_call_details, iter((request,)), False, False)
        response = await continuation(new_details, next(new_request_iterator))
        return (await postprocess(response)) if postprocess else response

    async def intercept_unary_stream(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = await \
            self._fn(client_call_details, iter((request,)), False, True)
        response_it = await continuation(new_details, next(new_request_iterator))
        return (await postprocess(response_it)) if postprocess else response_it

    async def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = await \
            self._fn(client_call_details, request_iterator, True, False)
        response = await continuation(new_details, new_request_iterator)
        return (await postprocess(response)) if postprocess else response

    async def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = await \
            self._fn(client_call_details, request_iterator, True, True)
        response_it = await continuation(new_details, new_request_iterator)
        return (await postprocess(response_it)) if postprocess else response_it


def create(intercept_async_call):
    return _ClientInterceptorAsync(intercept_async_call)


ClientCallDetails = namedtuple('ClientCallDetails', ('method', 'timeout', 'metadata', 'credentials'))


def header_adder_interceptor_async(header, value):
    async def intercept_async_call(client_call_details, request_iterator, request_streaming, response_streaming):
        metadata = list(client_call_details.metadata or ())
        metadata.append((header, value))
        client_call_details = ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata, client_call_details.credentials,
        )
        return client_call_details, request_iterator, None

    return create(intercept_async_call)

#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import inspect
from functools import wraps
from typing import List

from stackinsights import Layer, Component
from stackinsights.trace.context import get_context
from stackinsights.trace.tags import Tag


def trace(
        op: str = None,
        layer: Layer = Layer.Unknown,
        component: Component = Component.Unknown,
        tags: List[Tag] = None,
):
    def decorator(func):
        _op = op or func.__name__

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                context = get_context()
                span = context.new_local_span(op=_op)
                span.layer = layer
                span.component = component
                if tags:
                    for tag in tags:
                        span.tag(tag)
                with span:
                    return await func(*args, **kwargs)

            return wrapper

        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                context = get_context()
                span = context.new_local_span(op=_op)
                span.layer = layer
                span.component = component
                if tags:
                    for tag in tags:
                        span.tag(tag)
                with span:
                    return func(*args, **kwargs)

            return wrapper

    return decorator


def runnable(
        op: str = None,
        layer: Layer = Layer.Unknown,
        component: Component = Component.Unknown,
        tags: List[Tag] = None,
):
    def decorator(func):
        snapshot = get_context().capture()

        @wraps(func)
        def wrapper(*args, **kwargs):
            _op = op or f'Thread/{func.__name__}'
            context = get_context()
            with context.new_local_span(op=_op) as span:
                context.continued(snapshot)
                span.layer = layer
                span.component = component
                if tags:
                    for tag in tags:
                        span.tag(tag)
                func(*args, **kwargs)

        return wrapper

    return decorator

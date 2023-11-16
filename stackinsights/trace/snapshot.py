#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stackinsights.trace.context import SpanContext

from stackinsights.trace import ID


class Snapshot:
    def __init__(
            self,
            segment_id: str = None,
            span_id: int = None,
            trace_id: ID = None,
            endpoint: str = None,
            correlation: dict = None
    ):
        self.trace_id = trace_id  # type: ID
        self.segment_id = segment_id  # type: str
        self.span_id = span_id  # type: int
        self.endpoint = endpoint  # type: str
        self.correlation = correlation.copy()  # type: dict

    def is_from_current(self, context: 'SpanContext'):
        return self.segment_id is not None and self.segment_id == context.capture().segment_id

    def is_valid(self):
        return self.segment_id is not None and self.span_id > -1 and self.trace_id is not None

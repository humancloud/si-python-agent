#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time
from collections import defaultdict
from typing import List, Union, DefaultDict
from typing import TYPE_CHECKING

from stackinsights import Kind, Layer, Log, Component, LogItem, config
from stackinsights.trace import ID
from stackinsights.trace.carrier import Carrier
from stackinsights.trace.segment import SegmentRef, Segment
from stackinsights.trace.tags import Tag
from stackinsights.utils.lang import tostring
from stackinsights.utils.exception import IllegalStateError

if TYPE_CHECKING:
    from stackinsights.trace.context import SpanContext


@tostring
class Span:
    def __init__(
            self,
            context: 'SpanContext',
            sid: int = -1,
            pid: int = -1,
            op: str = None,
            peer: str = None,
            kind: Kind = None,
            component: Component = None,
            layer: Layer = None,
    ):
        self._depth = 0
        self.context = context  # type: SpanContext
        self.sid = sid  # type: int
        self.pid = pid  # type: int
        self.op = op  # type: str
        self.peer = peer  # type: str
        self.kind = kind  # type: Kind
        self.component = component or Component.Unknown  # type: Component
        self.layer = layer or Layer.Unknown  # type: Layer
        self.inherit = Component.Unknown  # type: Component

        self.tags = defaultdict(list)  # type: DefaultDict[str, Union[Tag, List[Tag]]]
        self.logs = []  # type: List[Log]
        self.refs = []  # type: List[SegmentRef]
        self.start_time = 0  # type: int
        self.end_time = 0  # type: int
        self.error_occurred = False  # type: bool

    @property
    def depth(self):
        return self._depth

    def start(self):
        self._depth += 1
        if self._depth != 1:
            return

        self.start_time = int(time.time() * 1000)
        self.context.start(self)

    def stop(self):
        self._depth -= 1
        if self._depth:
            return False

        return self.context.stop(self)

    def finish(self, segment: 'Segment') -> bool:
        self.end_time = int(time.time() * 1000)
        segment.archive(self)
        return True

    def raised(self) -> 'Span':
        from stackinsights.utils.filter import sw_traceback
        self.error_occurred = True
        self.logs = [Log(items=[
            LogItem(key='Traceback', val=sw_traceback()),
        ])]
        return self

    def log(self, ex: Exception) -> 'Span':
        self.error_occurred = True
        self.logs.append(Log(items=[LogItem(key='Traceback', val=str(ex))]))
        return self

    def tag(self, tag: Tag) -> 'Span':
        if tag.overridable:
            self.tags[tag.key] = tag
        else:
            self.tags[tag.key].append(tag)

        return self

    def iter_tags(self):
        for tag in self.tags.values():
            if isinstance(tag, Tag):
                yield tag
            else:
                yield from tag

    def inject(self) -> 'Carrier':
        raise IllegalStateError(
            'can only inject context carrier into ExitSpan, this may be a potential bug in the agent, '
            'please report this in https://github.com/apache/stackinsights/issues if you encounter this. '
        )

    def extract(self, carrier: 'Carrier') -> 'Span':
        if carrier is None:
            return self

        self.context.segment.relate(ID(carrier.trace_id))
        self.context._correlation = carrier.correlation_carrier.correlation

        if not carrier.is_valid:
            return self

        ref = SegmentRef(carrier=carrier)

        if ref not in self.refs:
            self.refs.append(ref)

        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.raised()
        self.stop()
        if exc_tb is not None:
            return False
        return True


@tostring
class EntrySpan(Span):
    def __init__(
            self,
            context: 'SpanContext',
            sid: int = -1,
            pid: int = -1,
            op: str = None,
            peer: str = None,
            component: 'Component' = None,
            layer: 'Layer' = None,
    ):
        Span.__init__(
            self,
            context,
            sid,
            pid,
            op,
            peer,
            Kind.Entry,
            component,
            layer,
        )
        self._max_depth = 0

    def start(self):
        Span.start(self)
        self._max_depth = self._depth
        self.component = Component.Unknown
        self.layer = Layer.Unknown
        self.logs = []
        self.tags = defaultdict(list)


@tostring
class ExitSpan(Span):
    def __init__(
            self,
            context: 'SpanContext',
            sid: int = -1,
            pid: int = -1,
            op: str = None,
            peer: str = None,
            component: 'Component' = None,
            layer: 'Layer' = None,
    ):
        Span.__init__(
            self,
            context,
            sid,
            pid,
            op,
            peer,
            Kind.Exit,
            component,
            layer,
        )

    def inject(self) -> 'Carrier':
        return Carrier(
            trace_id=str(self.context.segment.related_traces[0]),
            segment_id=str(self.context.segment.segment_id),
            span_id=str(self.sid),
            service=config.agent_name,
            service_instance=config.agent_instance_name,
            endpoint=self.op,
            client_address=self.peer,
            correlation=self.context._correlation,
        )


@tostring
class NoopSpan(Span):
    def __init__(self, context: 'SpanContext' = None):
        Span.__init__(self, context=context, op='', kind=Kind.Local)

    def extract(self, carrier: 'Carrier'):
        return

    def inject(self) -> 'Carrier':
        return Carrier()

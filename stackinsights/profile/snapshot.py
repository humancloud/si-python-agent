#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from typing import List

from stackinsights.protocol.profile.Profile_pb2 import ThreadSnapshot, ThreadStack


class TracingThreadSnapshot:

    def __init__(self, task_id: str, trace_segment_id: str, sequence: int, time: int, stack_list: List[str]):
        self.task_id = task_id
        self.trace_segment_id = trace_segment_id
        self.sequence = sequence
        self.time = time
        self.stack_list = stack_list

    def transform(self) -> ThreadSnapshot:
        code_sigs = list(self.stack_list)
        stack = ThreadStack(codeSignatures=code_sigs)

        snapshot = ThreadSnapshot(
            taskId=str(self.task_id),
            traceSegmentId=str(self.trace_segment_id),
            time=int(self.time),
            sequence=int(self.sequence),
            stack=stack
        )

        return snapshot

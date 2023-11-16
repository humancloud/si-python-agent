#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights.utils.lang import tostring


@tostring
class ProfileTask:

    def __init__(self,
                 task_id: str = '',
                 first_span_op_name: str = '',
                 duration: int = -1,
                 min_duration_threshold: int = -1,
                 thread_dump_period: int = -1,
                 max_sampling_count: int = -1,
                 start_time: int = -1,
                 create_time: int = -1):
        self.task_id = str(task_id)  # type: str
        self.first_span_op_name = str(first_span_op_name)  # type: str
        self.duration = int(duration)  # type: int
        # when can start profile after span context created
        self.min_duration_threshold = int(min_duration_threshold)  # type: int
        # profile interval
        self.thread_dump_period = int(thread_dump_period)  # type: int
        self.max_sampling_count = int(max_sampling_count)  # type: int
        self.start_time = int(start_time)  # type: int
        self.create_time = int(create_time)  # type: int

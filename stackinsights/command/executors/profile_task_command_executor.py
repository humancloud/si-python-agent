#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights.command.executors.command_executor import CommandExecutor
from stackinsights.command.profile_task_command import ProfileTaskCommand
from stackinsights import profile
from stackinsights.profile.profile_task import ProfileTask


class ProfileTaskCommandExecutor(CommandExecutor):

    def execute(self, command: ProfileTaskCommand):
        profile_task = ProfileTask(task_id=command.task_id,
                                   first_span_op_name=command.endpoint_name,
                                   duration=command.duration,
                                   min_duration_threshold=command.min_duration_threshold,
                                   thread_dump_period=command.dump_period,
                                   max_sampling_count=command.max_sampling_count,
                                   start_time=command.start_time,
                                   create_time=command.create_time)

        profile.profile_task_execution_service.add_profile_task(profile_task)

#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

profile_task_execution_service = None


def init():
    from stackinsights.profile.profile_service import ProfileTaskExecutionService

    global profile_task_execution_service
    if profile_task_execution_service:
        return

    profile_task_execution_service = ProfileTaskExecutionService()

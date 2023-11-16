#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from stackinsights.command.base_command import BaseCommand
from stackinsights.command.executors.command_executor import CommandExecutor


class NoopCommandExecutor(CommandExecutor):
    def __init__(self):
        pass

    def execute(self, command: BaseCommand):
        pass

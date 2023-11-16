#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import queue
from asyncio import Queue as AsyncQueue, QueueFull as AsyncQueueFull
from collections import deque

from stackinsights.protocol.common.Command_pb2 import Commands, Command

from stackinsights.command.base_command import BaseCommand
from stackinsights.command.executors import noop_command_executor_instance
from stackinsights.command.executors.profile_task_command_executor import ProfileTaskCommandExecutor
from stackinsights.command.profile_task_command import ProfileTaskCommand
from stackinsights.loggings import logger


class CommandService:

    def __init__(self):
        self._commands = queue.Queue()  # type: queue.Queue
        # don't execute same command twice
        self._command_serial_number_cache = CommandSerialNumberCache()

    def dispatch(self):
        while True:
            # block until a command is available
            command = self._commands.get()  # type: BaseCommand
            if not self.__is_command_executed(command):
                command_executor_service.execute(command)
                self._command_serial_number_cache.add(command.serial_number)

    def __is_command_executed(self, command: BaseCommand):
        return self._command_serial_number_cache.contains(command.serial_number)

    def receive_command(self, commands: Commands):
        for command in commands.commands:
            try:
                base_command = CommandDeserializer.deserialize(command)
                logger.debug('received command [{%s} {%s}]', base_command.command, base_command.serial_number)

                if self.__is_command_executed(base_command):
                    logger.warning('command[{%s}] is executed, ignored.', base_command.command)
                    continue

                try:
                    self._commands.put(base_command)
                except queue.Full:
                    logger.warning('command[{%s}, {%s}] cannot add to command list. because the command list is full.',
                                   base_command.command, base_command.serial_number)
            except UnsupportedCommandException as e:
                logger.warning('received unsupported command[{%s}].', e.command.command)


class CommandServiceAsync:

    def __init__(self):
        self._commands = AsyncQueue()  # type: AsyncQueue
        # don't execute same command twice
        self._command_serial_number_cache = CommandSerialNumberCache()

    async def dispatch(self):
        while True:
            # block until a command is available
            command = await self._commands.get()  # type: BaseCommand
            if not self.__is_command_executed(command):
                command_executor_service.execute(command)
                self._command_serial_number_cache.add(command.serial_number)

    def __is_command_executed(self, command: BaseCommand):
        return self._command_serial_number_cache.contains(command.serial_number)

    def receive_command(self, commands: Commands):
        for command in commands.commands:
            try:
                base_command = CommandDeserializer.deserialize(command)
                logger.debug('received command [{%s} {%s}]', base_command.command, base_command.serial_number)

                if self.__is_command_executed(base_command):
                    logger.warning('command[{%s}] is executed, ignored.', base_command.command)
                    continue

                try:
                    self._commands.put_nowait(base_command)
                except AsyncQueueFull:
                    logger.warning(
                        'command[{%s}, {%s}] cannot add to command list. because the command list is full.',
                        base_command.command,
                        base_command.serial_number)
            except UnsupportedCommandException as e:
                logger.warning('received unsupported command[{%s}].', e.command.command)


class CommandSerialNumberCache:

    def __init__(self, maxlen=64):
        self.queue = deque(maxlen=maxlen)

    def add(self, number: str):
        # Once a bounded length deque is full, when new items are added,
        # a corresponding number of items are discarded from the opposite end.
        self.queue.append(number)

    def contains(self, number: str) -> bool:
        try:
            _ = self.queue.index(number)
            return True
        except ValueError:
            return False


class CommandExecutorService:
    """
    route commands to appropriate executor
    """

    def __init__(self):
        self.__command_executor_map = {ProfileTaskCommand.NAME: ProfileTaskCommandExecutor()}

    def execute(self, command: BaseCommand):
        self.__executor_for_command(command).execute(command)

    def __executor_for_command(self, command: BaseCommand):
        executor = self.__command_executor_map.get(command.command)
        if not executor:
            return noop_command_executor_instance
        return executor


class CommandDeserializer:

    @staticmethod
    def deserialize(command: Command) -> BaseCommand:
        command_name = command.command

        if ProfileTaskCommand.NAME == command_name:
            return ProfileTaskCommand.deserialize(command)
        else:
            raise UnsupportedCommandException(command)


class UnsupportedCommandException(Exception):

    def __init__(self, command):
        self.command = command


# init
command_executor_service = CommandExecutorService()

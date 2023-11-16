#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#


class BaseCommand:
    def __init__(self,
                 command: str = '',
                 serial_number: str = ''):
        self.command = command  # type: str
        self.serial_number = serial_number  # type: str

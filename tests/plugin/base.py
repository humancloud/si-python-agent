#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import time
import inspect
import os
import sys
from difflib import Differ
from os.path import dirname

import requests
import yaml
from requests import Response

try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader


class TestPluginBase:
    def validate(self, expected_file_name=None):
        # type: (str) -> Response

        if expected_file_name is None:
            expected_file_name = os.path.join(dirname(inspect.getfile(self.__class__)), 'expected.data.yml')

        with open(expected_file_name) as expected_data_file:
            expected_data = os.linesep.join(expected_data_file.readlines())

            response = requests.post(url='http://localhost:12800/dataValidate', data=expected_data)

            if response.status_code != 200:
                # heuristically retry once
                time.sleep(10)
                response = requests.post(url='http://localhost:12800/dataValidate', data=expected_data)

            if response.status_code != 200:
                res = requests.get('http://localhost:12800/receiveData')

                actual_data = yaml.dump(yaml.load(res.content, Loader=Loader))

                differ = Differ()
                diff_list = list(differ.compare(
                    actual_data.splitlines(keepends=True),
                    yaml.dump(yaml.load(expected_data, Loader=Loader)).splitlines(keepends=True)
                ))

                print('diff list: ')

                sys.stdout.writelines(diff_list)
            assert response.status_code == 200

            return response

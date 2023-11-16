#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from typing import Callable

import pytest
import requests

from tests.plugin.base import TestPluginBase


@pytest.fixture
def prepare():
    # type: () -> Callable
    return lambda *_: requests.post('http://0.0.0.0:9090', timeout=5)


class TestPlugin(TestPluginBase):
    def test_plugin(self, docker_compose, version):
        self.validate()

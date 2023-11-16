#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from typing import Callable

import pytest
import requests

from stackinsights.plugins.sw_aiohttp import support_matrix
from tests.orchestrator import get_test_vector
from tests.plugin.base import TestPluginBase


@pytest.fixture  # pyre-ignore
def prepare():
    # type: () -> Callable
    return lambda *_: requests.get('http://0.0.0.0:9090/stackinsights', timeout=5)


class TestPlugin(TestPluginBase):
    @pytest.mark.parametrize('version', get_test_vector(lib_name='aiohttp', support_matrix=support_matrix))
    def test_plugin(self, docker_compose, version):
        self.validate()
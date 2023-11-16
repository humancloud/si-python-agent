#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from typing import Callable

import pytest
import requests

from stackinsights.plugins.sw_flask import support_matrix
from tests.orchestrator import get_test_vector
from tests.plugin.base import TestPluginBase


@pytest.fixture
def prepare():
    # type: () -> Callable
    return lambda *_: requests.get('http://0.0.0.0:9090/users?test=test1&test=test2&test2=test2', timeout=5)


class TestPlugin(TestPluginBase):
    @pytest.mark.parametrize('version', get_test_vector(lib_name='flask', support_matrix=support_matrix))
    def test_plugin(self, docker_compose, version):
        self.validate()

        response = requests.get('http://0.0.0.0:9090/users', timeout=5)
        assert response.status_code == 200
        assert response.json()['correlation'] == 'correlation'
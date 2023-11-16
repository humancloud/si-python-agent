#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import unittest
from stackinsights.utils.filter import sw_urlparse, sw_filter


class TestFilter(unittest.TestCase):
    def test_url_parse(self):
        self.assertEqual(sw_urlparse('http://localhost:8080').geturl(), 'http://localhost:8080')
        self.assertEqual(sw_urlparse('https://localhost:8080').geturl(), 'https://localhost:8080')
        self.assertEqual(sw_urlparse('http://user:password@localhost:8080').geturl(), 'http://localhost:8080')
        self.assertEqual(sw_urlparse('https://user:password@localhost:8080').geturl(), 'https://localhost:8080')
        self.assertEqual(sw_urlparse('ws://user:password@localhost:8080/ws').geturl(), 'ws://localhost:8080/ws')
        self.assertEqual(sw_urlparse('wss://user:password@localhost:8080/ws').geturl(), 'wss://localhost:8080/ws')

    def test_log_filter(self):
        from stackinsights import config
        config.agent_log_reporter_safe_mode = True

        self.assertEqual(
            'user:password not in http://localhost:8080',
            sw_filter('user:password not in http://localhost:8080')
        )
        self.assertEqual(
            'user:password in http://localhost:8080',
            sw_filter('user:password in http://user:password@localhost:8080')
        )
        self.assertEqual(
            'http://localhost:8080 contains user:password',
            sw_filter('http://user:password@localhost:8080 contains user:password')
        )
        self.assertEqual(
            'DATETIMEhttp://localhost:8080 contains user:password',
            sw_filter('DATETIMEhttp://user:password@localhost:8080 contains user:password')
        )


if __name__ == '__main__':
    unittest.main()

#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import unittest

from packaging import version

from stackinsights.plugins import check
from stackinsights.utils.comparator import operators


class TestVersionCheck(unittest.TestCase):
    def test_operators(self):
        # <
        f = operators.get('<')
        v1 = version.parse('1.0.0')
        v2 = version.parse('1.0.1')
        self.assertTrue(f(v1, v2))
        self.assertFalse(f(v2, v1))

        v2 = version.parse('1.0.0')
        self.assertFalse(f(v1, v2))

        # <=
        f = operators.get('<=')
        v1 = version.parse('1.0')
        v2 = version.parse('1.0')
        self.assertTrue(v1, v2)

        v2 = version.parse('1.1.0')
        self.assertTrue(f(v1, v2))
        self.assertFalse(f(v2, v1))

        # =
        f = operators.get('==')
        v1 = version.parse('1.0.0')
        v2 = version.parse('1.0.0')
        self.assertTrue(f(v1, v2))

        v2 = version.parse('1.0.1')
        self.assertFalse(f(v1, v2))

        # >=
        f = operators.get('>=')
        v1 = version.parse('1.0.0')
        v2 = version.parse('1.0.0')
        self.assertTrue(f(v1, v2))

        v2 = version.parse('1.0.1')
        self.assertFalse(f(v1, v2))
        self.assertTrue(f(v2, v1))

        # >
        f = operators.get('>')
        v1 = version.parse('1.0.0')
        v2 = version.parse('1.0.1')
        self.assertFalse(f(v1, v2))
        self.assertTrue(f(v2, v1))

        v2 = version.parse('1.0.0')
        self.assertFalse(f(v1, v2))

        # !=
        f = operators.get('!=')
        v1 = version.parse('1.0.0')
        v2 = version.parse('1.0.1')
        self.assertTrue(f(v1, v2))

        v2 = version.parse('1.0.0')
        self.assertFalse(f(v1, v2))

    def test_version_check(self):
        current_version = version.parse('1.8.0')

        self.assertTrue(check('>1.1.0', current_version))
        self.assertTrue(check('>=1.0.0', current_version))
        self.assertTrue(check('<2.0.0', current_version))
        self.assertTrue(check('<=1.8.0', current_version))
        self.assertTrue(check('==1.8.0', current_version))
        self.assertTrue(check('!=1.6.0', current_version))

        self.assertFalse(check('>1.9.0', current_version))
        self.assertFalse(check('>=1.8.1', current_version))
        self.assertFalse(check('<1.8.0', current_version))
        self.assertFalse(check('<=1.7.0', current_version))
        self.assertFalse(check('==1.0.0', current_version))
        self.assertFalse(check('!=1.8.0', current_version))


if __name__ == '__main__':
    unittest.main()

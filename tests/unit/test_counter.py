#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import threading
import unittest

from stackinsights.utils.counter import AtomicCounter


class TestAtomicCounter(unittest.TestCase):
    def test_counter(self):
        counter = AtomicCounter()

        threads = [threading.Thread(target=lambda: counter.next()) for _ in range(0, 2000)]

        [t.start() for t in threads]

        [t.join() for t in threads]

        self.assertEqual(1999, counter.value)


if __name__ == '__main__':
    unittest.main()

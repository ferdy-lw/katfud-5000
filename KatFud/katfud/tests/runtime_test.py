import os
import time
import unittest

from pyramid import testing
# from pudb import set_trace; set_trace()


class RunTimeTests(unittest.TestCase):
    def setUp(self):
        # from katfud import main
        # app = main({}, **{'katfud.conf_file': 'conf.yml', 'katfud.non_pi': True})
        testing.setUp()

        import katfud.runtime as runtime

        self.test_runtime = runtime._Runtime(os.path.join(os.path.dirname(__file__), 'runtime_test.yml'))

    def tearDown(self):
        testing.tearDown()

    def test_runtime(self):

        self.assertTrue(self.test_runtime.is_feed_time())

    def test_runtime_next(self):

        self.assertTrue(self.test_runtime.is_feed_time(True))

        time.sleep(2)
        self.assertFalse(self.test_runtime.is_feed_time(True))

        time.sleep(1)
        self.assertFalse(self.test_runtime.is_feed_time(True))
        time.sleep(2)
        self.assertTrue(self.test_runtime.is_feed_time(True))
        self.assertFalse(self.test_runtime.is_feed_time(True))


if __name__ == '__main__':
    unittest.main()

import unittest
from . import settings


class TestSettings(unittest.TestCase):
    def test_debug(self):
        self.assertTrue(settings.DEBUG)


if __name__ == '__main__':
    unittest.main()

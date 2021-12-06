from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock


class test_services(unittest.TestCase):
    def setUp(self) -> None:
        # set up
        self.test_services = True
        pass
    def tearDown(self) -> None:
        # clean up
        pass

    def test_boolean(self):
        self.assertTrue(self.test_services)
    

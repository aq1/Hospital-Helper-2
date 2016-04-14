import unittest

from app.model.logic import AllowedModule


class TestAllowedModule(unittest.TestCase):

    def test_module_storage(self):
        import math
        allowed_module = AllowedModule(math)
        assert issubclass(allowed_module, list)

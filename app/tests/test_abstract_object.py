import unittest

from app.logic.abstract_logic_obj import AbstractObject


class TestAbstractObj(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(AssertionError):
            AbstractObject(name='Test', args=['arg'])

    def test_get(self):
        obj = AbstractObject(name='Test', args=[['arg']])
        self.assertEqual(obj.get('arg'), 0)

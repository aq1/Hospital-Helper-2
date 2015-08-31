import unittest

from app.logic.calculable_object import CalculableObject


class TestCalculableObject(unittest.TestCase):

    def setUp(self):
        args_a = {'name': 'ObjectA',
                  'args': [['arg0'],
                           ['arg1', 'arg0 + 2'],
                           ['arg2', 'arg1 + sqrt(9)'],
                           ['arg3', 'arg2 / len("12345")'],
                           ['arg4', 'arg3 * int("25")']]}

        args_b = {'name': 'ObjectB',
                  'args': [['arg0', 'arg4 + 1']]}

        self.object_a = CalculableObject(
            name=args_a['name'], args=args_a['args'])
        self.object_b = CalculableObject(
            name=args_b['name'], args=args_b['args'])

    def test_calculation(self):
        self.object_a.calculate()
        self.object_b.calculate()

        self.assertEqual(self.object_a['arg1'], 2)
        self.assertEqual(self.object_a['arg2'], 5)
        self.assertEqual(self.object_a['arg3'], 1)
        self.assertEqual(self.object_a['arg4'], 25)

        self.assertEqual(self.object_b['arg0'], 26)

    def test_repr(self):
        self.object_b['arg0'] = 0
        object_b_repr = str(self.object_b)
        repr_str = 'objectb\n\targ0: 0\n\n\tself["arg0"] = self._get_from_mediator("arg4") + 1'
        self.assertEqual(object_b_repr, repr_str)

import unittest

from app.logic.organ_factory import OrganFactory


class TestOrgan(unittest.TestCase):

    def setUp(self):
        args = {'name': 'TestOrgan',
                'args': [['arg0'],
                         ['arg1', 'arg0 + 2']]}

        self.organ = OrganFactory().create_organ(args=args)

    def test_calculate(self):
        self.organ.calculate()
        self.assertEqual(self.organ.arg1, 2)

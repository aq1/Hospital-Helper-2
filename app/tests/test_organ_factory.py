import unittest

from app.logic.organ_factory import OrganFactory
from app.logic.organ import Organ


class TestOrganFactory(unittest.TestCase):

    def test_many_organs_creation(self):
        organs = {'organs': [{'name': 'Heart',
                              'args': [['aorta'],
                                       ['KDO', 'aorta + LP * 2'],
                                       ['OAK'],
                                       ['LP'],
                                       ['MGP', 'aorta + OAK + bsa'],
                                       ['KDRLG']],
                              },
                             {'name': 'Pancreas',
                              'args': [['arg0', 'arg1+arg2+arg3*arg4'],
                                       ['arg1', 'arg2 + arg1 + from_mediator'],
                                       ['arg2'],
                                       ['arg3'],
                                       ['arg4']]}]}

        organ_factory = OrganFactory(organs['organs'])
        self.assertEqual(len(organ_factory.organs), len(organs['organs']))
        self.assertIsInstance(organ_factory.organs[0], Organ)
        self.assertIsInstance(organ_factory.organs[1], Organ)

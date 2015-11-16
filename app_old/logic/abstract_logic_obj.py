# -*- coding: UTF-8 -*-

import collections
import unidecode

from . import Mediator
from . import Parser


class AbstractObject(collections.OrderedDict, Parser):

    def __init__(self, name, args):

        super(AbstractObject, self).__init__()

        self.name = self._unidecode(name)
        self.calculation = []
        self.mediator = Mediator(self)

        calculations_to_add = []

        for arg in args:
            assert isinstance(arg, (tuple, list))
            key = self._unidecode(arg[0])
            try:
                calculation = arg[1]
            except IndexError:
                pass
            else:
                calculations_to_add.append((key, calculation))

            self[key] = 0

        for key, calculation in calculations_to_add:
            self._add_calculation(key, calculation)

    def _add_calculation(self, key, calculation):
        self.calculation.append(self.str_to_calculation(key, calculation))

    def _unidecode(self, value):
        return unidecode.unidecode(value.lower().replace(' ', '_'))

    def _get_from_mediator(self, key):
        return self.mediator.get(key)

    def __repr__(self):
        name = self.name
        items = ''.join(['\n\t{}: {}'.format(key, val)
                         for key, val in self.items()])
        calculation = ''.join(['\n\t{}'.format(calc)
                               for calc in self.calculation])
        return '{}{}\n{}'.format(name, items, calculation)

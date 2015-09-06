# -*- coding: UTF-8 -*-

import math
import builtins
import traceback

from . import AbstractObject


class CalculableObject(AbstractObject):

    '''
    Represents a single organ that contains its name
    and list of arguments. If argument has it second value
    then it's calculable and class will calculate the expression.
    '''

    def calculate(self):
        for expr in self.calculation:
            try:
                exec(expr)
            except Exception as e:
                print('{} in "{}"'.format(e, expr))
                traceback.print_tb(e.__traceback__)

    def get_value(self, key):
        return self[key]

    def get_value_list(self):
        return [(key, value) for key, value in self.items()]

    def get_items(self):
        return dict(self.items())

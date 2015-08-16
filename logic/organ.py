# -*- coding: UTF-8 -*-


from abstract_logic_obj import AbstractObject
from mediator import Mediator


class Organ(AbstractObject):

    '''
    Represents a single organ that contains its name
    and list of arguments. If argument has it second value
    then it's calculable and class will calculate the expression.

    Objects of this class are created by OrganFactory class.
    '''

    def get_args_list(self):
        return self.args



# a = Organ(name='123', args=[['asd'], ['dsd', 'asd + asd']], mediator=Mediator())

# print(a.calculate())

# -*- coding: UTF-8 -*-


from app.logic.mediator import Mediator


class AbstractObject(object):

    '''
    Abstract class for Organ and Patient common features.
    '''

    def __init__(self, name, args):

        self.name = name
        self.args = args
        self.mediator = Mediator(self)

        for each in args:
            assert isinstance(each, (tuple, list))
            self.__dict__[each[0]] = 0

    def get(self, key):
        return self.__dict__[key]

    def calculate(self):
        for each in self.args:
            try:
                arg, expr = each
            except ValueError:
                continue

            try:
                exec(expr)
            except (NameError, ValueError, IndexError, AttributeError) as e:
                print('Error: "{}" in expression\n"{}"\nCannot calculate'.format(e, expr))

    def _get_value_from_mediator(self, key):
        return self.mediator.get_attr(key)

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __str__(self):
        args = []
        for i, each in enumerate(self.args):
            try:
                arg = '{}={}'.format(each[0], each[1])
            except IndexError:
                arg = each[0]

            args.append('{}: {}'.format(i, arg))

        return '{}:\n{}'.format(self.name, ';\n'.join(args))

    def __repr__(self):
        return '<class "{}: {}">'.format(self.__class__.__name__, self.name)

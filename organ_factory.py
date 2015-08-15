# -*- coding: UTF-8 -*-
from json_to_obj import JsonToObj


class Organ(object):

    '''
    Represents a single organ that contaions its name
    and list of arguments. If argument has it second value
    then it's calculable and class will calculate the expression.

    Objects of this class are created by OrganFactory class.
    '''

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def _get_value_from_mediator(self, key):
        return self.mediator.get(key)

    def calculate(self):
        for each in self.args:
            try:
                exec(each[0])
            except IndexError:
                continue

    def get_args_list(self):
        return self.args

    def __repr__(self):
        args = []
        for i, each in enumerate(self.args):
            try:
                arg = '{}={}'.format(each[0], each[1])
            except IndexError:
                arg = each[0]

            args.append('{}: {}'.format(i, arg))

        return '{}:\n{}'.format(self.name, ';\n'.join(args))

    def __str__(self):
        return self.__repr__()


class OrganFactory(object):

    '''
    Contains all organs objects.
    Delegates creation process to JsonToObj class (self.factory).
    '''

    def __init__(self, data=None):
        self.factory = JsonToObj(klass=Organ)

        if not data:
            self.organs = []
        else:
            self.organs = self.create_many_organs(data)

    def __check_if_list_is_unique(list_):
        seen = set()
        return not any(i in seen or seen.add(i) for i in list_)

    def create_organ(self, data):
        # data excepts to be a dict
        return self.factory.create_obj(data=data)

    def create_many_organs(self, data):
        out = []
        for organ in data:
            out.append(self.create_organ(organ))
        return out

    def __str_to_expr(self, string, indexes):
        # Mew. Too complicated i guess
        i = 0
        out = []

        for match in self.re.finditer(string):
            begin, end = match.span()
            group = match.group()
            try:
                replacement = 'self.args[{}]'.format(indexes[group])
            except KeyError:
                replacement = 'self._get_value_from_mediator("{}")'.format(group)

            out.append(string[i:begin])
            out.append(replacement)
            i = end

        return ''.join(out)

    def __convert_calculated_args_expression(self, args):
        # TODO: Replace exec with secure mechanism.
        # Maybe it's going to be a simple lexical analyzer

        indexes = {arg[0]: i for (i, arg) in enumerate(args)}
        organ_args = []

        for each in args:
            try:
                arg, expr = each
            except ValueError:
                # No second argument == value will not be calculated
                organ_args.append(each)
                continue

            organ_args.append((arg, self.__str_to_expr(expr, indexes)))

        return organ_args

    def __repr__(self):
        return 'Organs:\n{}'.format('\n'.join(map(str, self.organs)))


if __name__ == '__main__':

    pass

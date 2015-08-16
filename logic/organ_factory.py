# -*- coding: UTF-8 -*-


from json_to_obj import JsonToObj
from organ import Organ
from mediator import Mediator


class OrganFactory(object):

    '''
    Contains all organs objects.
    Delegates creation process to JsonToObj class (self.factory).
    '''

    def __init__(self, args=None):
        self.factory = JsonToObj(klass=Organ)

        if not args:
            self.organs = []
        else:
            self.organs = self.create_many_organs(args)

    def __check_if_list_is_unique(list_):
        seen = set()
        return not any(i in seen or seen.add(i) for i in list_)

    def create_organ(self, args):
        # args excepts to be a dict
        return self.factory.create_obj(args=args)

    def create_many_organs(self, args):
        out = []
        for organ in args:
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
    import json

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

    organs = organs['organs']

    organ_factory = OrganFactory(organs)
    a = organ_factory.organs[0]
    a.calculate()

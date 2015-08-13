import json
import re
import pprint


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

    def calculate(self):
        for each in self.args:
            try:
                exec(each[0])
            except IndexError:
                continue

    def get_args_list(self):
        return self.args


class OrganFactory(object):

    '''
    Translates json object to an Organ objects.

    It's meant that json is generated initially by programmer
    and can be edited by user, so there has to be an automatic
    process that creates objects.
    '''

    def __init__(self):
        self.organs = []
        self.re = re.compile(r'[a-zA-Z]+[a-zA-Z0-9\-_]*')

    def __check_if_list_is_unique(list_):
        seen = set()
        return not any(i in seen or seen.add(i) for i in list_)

    def create_organ(self, json_data):
        data = json.loads(json_data)
        self.__convert_calculated_args_expression(data['args'])

    def _get_value_from_mediator(self, key):
        return self.mediator.get(key)

    def __convert_calculated_args_expression(self, args):
        # TODO: Replace exec with secure mechanism.
        # Maybe it's going to be a simple lexical analyzer

        indexes = {arg[0]: i for (i, arg) in enumerate(args)}

        for each in args:
            try:
                arg, expr = each
            except ValueError:
                # No second argument == value will not be calculated
                continue

            i = 0
            out = []
            for match in self.re.finditer(expr):
                begin, end = match.span()
                group = match.group()
                try:
                    replacement = 'self.args[{}]'.format(indexes[group])
                except KeyError:
                    replacement = 'self._get_value_from_mediator("{}")'.format(group)

                out.append(expr[i:begin])
                out.append(replacement)
                i = end

                # Mew. Too complicated i guess
                # group = match.group()
                # expr = expr.replace(group, 'self.args[{}]'.format(arg_index))

            print(''.join(out))


if __name__ == '__main__':

    organs = {'organs': [{'name': 'Heart',
                          'args': [['aorta'],
                                   ['KDO', 'aorta + LP * 2'],
                                   ['OAK'],
                                   ['LP'],
                                   ['MGP', 'aorta + OAK + bsa'],
                                   ['KDRLG']],
                          }]}
    pprint.pprint(organs)

    organ_factory = OrganFactory()
    organ_factory.create_organ(json.dumps(organs['organs'][0]))

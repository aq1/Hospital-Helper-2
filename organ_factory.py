import json
import pprint


organs = {'organs': [{'name': 'Heart',
                      'args': [['aorta'],
                               ['KDO', 'KDRLG + LP * 2'],
                               ['OAK'],
                               ['LP'],
                               ['MGP', 'aorta + OAK'],
                               ['KDRLG']],
                      }]}
pprint.pprint(organs)


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

    def __check_if_list_is_unique(list_):
        seen = set()
        return not any(i in seen or seen.add(i) for i in list_)

    def create_organ(self, json_data):
        pass

    def convert_calculated_args_expression(self, args):
        # TODO: Replace exec with secure mechanism.
        # Maybe it's going to be a simple lexical analyzer
        for each in args:
            try:
                arg, expr = each
            except IndexError:
                # No second argument == value is not calculated
                continue


# organ_factory = OrganFactory()
# organ_factory.create_organ(json.dumps(organs['organs'][0]))

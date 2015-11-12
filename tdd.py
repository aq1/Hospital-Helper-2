import re
import math
import builtins
from collections import OrderedDict

modules = math, builtins


class Mediator:

    def __init__(self, objects=None):

        if objects is None:
            objects = []

        self.objects = objects

    def _get_value(self, name):
        for obj in self.objects:
            try:
                return obj[name]
            except KeyError:
                continue

        raise AttributeError('Name {} was not found in objects'.format(name))

    def get(self, key):
        try:
            obj, name = key.split('.')
        except IndexError:
            name = key

        return self._get_value(name)

    def __call__(self, obj):
        self.objects.append(obj)
        return self


class AllowedModule(list):

    excluded_attr = ('exec', 'eval')

    def __init__(self, module):
        self.name = module.__name__
        super().__init__(
            [attr for attr in dir(module) if attr not in self.excluded_attr])


ALLOWED_MODULES = [AllowedModule(module) for module in modules]


class Parser:

    property_re = re.compile(r'[^\W\d]+\.?[\w\-_]*', re.UNICODE)
    module_str = '{}.{}'
    get_str = 'self._get("{}")'
    self_str = 'self._set("{}", {})'

    @classmethod
    def parse_calculation_string(cls, name, string):
        out = []
        i = 0

        for match in cls.property_re.finditer(string):
            begin, end = match.span()
            group = match.group()

            for module in ALLOWED_MODULES:
                if group in module:
                    group = cls.module_str.format(module.name, group)
                    break
            else:
                group = cls.get_str.format(group)

            out.append(''.join((string[i:begin], group)))
            i = end
        else:
            out.append(string[i:])

        expr = ''.join([chunk for chunk in out])
        return cls.self_str.format(name, expr)


class CalculableObject(OrderedDict):

    def __init__(self, name, args, parser, mediator):
        super().__init__()

        self.name = name
        self.mediator = mediator(self)
        self.calculations = []

        for each in args:
            self[each['name']] = 5
            calculation = each.get('calculation')
            if calculation:
                self.calculations.append(
                    parser.parse_calculation_string(each['name'], calculation))

        self.calculations = '\n'.join(self.calculations)

    def _set(self, name, value):
        if not self.get(name):
            raise AttributeError('No such attribute: {}'.format(name))

        self[name] = value

    def _get(self, name):
        try:
            value = self[name]
        except KeyError:
            value = self.mediator.get(name)

        return value

    def _add_calculation(self, name, calculation):
        pass

    def calculate(self):
        print(self.calculations)
        exec(self.calculations)


def test_calc_obj():
    name = 'test'
    args = [{
        'name': 'arg0'
    },
        {
        'name': 'testarg0',
        'calculation': 'arg0 * 2 + arg1'
    },
        {
        'name': 'arg1'
    },
        {
        'name': 'testarg1',
        'calculation': 'arg1 * arg0 + arg1 + arg0 + sqrt(arg1)'
    }]

    name1 = 'test_test_2'

    args1 = [{
        'name': 'external_arg',
        'calculation': 'test.testarg1 + 2'
    }]

    parser = Parser()
    mediator = Mediator()
    c = CalculableObject(name, args, parser, mediator)
    c1 = CalculableObject(name1, args1, parser, mediator)

    c.calculate()
    c1.calculate()
    for k, v in c1.items():
        print(k, v)

test_calc_obj()

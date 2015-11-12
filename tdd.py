import sys
import re
import json
from collections import OrderedDict

import unidecode


STRUCTURE = """[{
    "name": "Клиент",
    "db": true,
    "args": [{
        "name": "Фамилия"
    }, {
        "name": "Имя"
    }, {
        "name": "Отчество"
    }, {
        "name": "Возраст"
    }, {
        "name": "Чсс"
    }, {
        "name": "Рост"
    }, {
        "name": "Вес"
    }, {
        "name": "_ППТ",
        "calculation": "sqrt(Рост * Вес / 3600)"
    }]
}, {
    "name": "Сердце",
    "args": [{
        "name": "Аорта"
    }, {
        "name": "ОАК"
    }, {
        "name": "ЛП"
    }, {
        "name": "КДРЛЖ"
    }, {
        "name": "КСРЛЖ"
    }, {
        "name": "ЗСЛЖ"
    }, {
        "name": "МЖП"
    }, {
        "name": "АК"
    }, {
        "name": "КЛА"
    }, {
        "name": "ПП"
    }, {
        "name": "ПЖ"
    }, {
        "name": "НПВ"
    }, {
        "name": "КДО",
        "calculation": "(7 / (2.4 + КДРЛЖ) * КДРЛЖ) ** 3"
    }, {
        "name": "КСО",
        "calculation": "(7 / (2.4 + КСРЛЖ) * КСРЛЖ) ** 3"
    }, {
        "name": "ФВ",
        "calculation": "((КДО - КСО) / КДО) * 100"
    }, {
        "name": "ИММЛЖ",
        "calculation": "(0.8 * (1.04 * (sum((КДРЛЖ, МЖП, ЗСЛЖ)) ** 3) - КДРЛЖ ** 3) + 0.6) / Клиент._ППТ"
    }, {
        "name": "ОТС",
        "calculation": "(2 * ЗСЛЖ) / КДРЛЖ"
    }]
}, {
    "name": "Печень",
    "args": [{
        "name": "КВР"
    }, {
        "name": "ВВ"
    }, {
        "name": "НПВ"
    }, {
        "name": "Холедох"
    }]
}, {
    "name": "Желчный",
    "args": [{
        "name": "Длина"
    }, {
        "name": "Ширина"
    }, {
        "name": "Толщина"
    }, {
        "name": "Стенка"
    }, {
        "name": "Объем",
        "calculation": "0.00052 * (Длина * Ширина * Толщина)"
    }]
}, {
    "name": "Поджелудочная",
    "args": [{
        "name": "Головка"
    }, {
        "name": "Тело"
    }, {
        "name": "Хвост"
    }, {
        "name": "Вирсунгов"
    }]
}, {
    "name": "Селезенка",
    "args": [{
        "name": "Длина"
    }, {
        "name": "Ширина"
    }, {
        "name": "Толщина"
    }, {
        "name": "Площадь"
    }]
}, {
    "name": "Почки",
    "args": [{
        "name": "Длина"
    }, {
        "name": "Ширина"
    }, {
        "name": "Паренхим"
    }, {
        "name": "Чашечки"
    }, {
        "name": "Лоханка"
    }, {
        "name": "Длина_2"
    }, {
        "name": "Ширина_2"
    }, {
        "name": "Паренхим_2"
    }, {
        "name": "Чашечки_2"
    }, {
        "name": "Лоханка_2"
    }]
}, {
    "name": "Щитовидная",
    "args": [{
        "name": "Перешеек"
    }, {
        "name": "Длина"
    }, {
        "name": "Ширина"
    }, {
        "name": "Толщина"
    }, {
        "name": "Объем",
        "calculation": "0.00048 * (Длина * Ширина * Толщина)"
    }, {
        "name": "Длина_2"
    }, {
        "name": "Ширина_2"
    }, {
        "name": "Толщина_2"
    }, {
        "name": "Объем_2",
        "calculation": "0.00048 * (Длина_2 * Ширина_2 * Толщина_2)"
    }, {
        "name": "V_общ",
        "calculation": "Объем + Объем_2"
    }]
}, {
    "name": "Предстательная",
    "args": [{
        "name": "Длина"
    }, {
        "name": "Ширина"
    }, {
        "name": "Толщина"
    }, {
        "name": "Объем",
        "calculation": "0.00052 * (Длина * Ширина * Толщина)"
    }]
}, {
    "name": "М.Пузырь",
    "args": [{
        "name": "Длина"
    }, {
        "name": "Ширина"
    }, {
        "name": "Толщина"
    }, {
        "name": "Стенка"
    }, {
        "name": "Объем",
        "calculation": "0.00052 * (Длина * Ширина * Толщина)"
    }]
}, {
    "name": "Гинекология",
    "args": []
}, {
    "name": "Образование",
    "args": [{
        "name": "Длина_1"
    }, {
        "name": "Длина_2"
    }, {
        "name": "Длина_3"
    }, {
        "name": "Длина_4"
    }, {
        "name": "Длина_5"
    }, {
        "name": "Длина_6"
    }]
}, {
    "name": "Киста",
    "args": [{
        "name": "Длина_1"
    }, {
        "name": "Длина_2"
    }, {
        "name": "Длина_3"
    }, {
        "name": "Длина_4"
    }, {
        "name": "Длина_5"
    }, {
        "name": "Длина_6"
    }, {
        "name": "Длина_7"
    }, {
        "name": "Длина_8"
    }]
}]"""


class Mediator:

    '''
    Sort of implementation of 'Mediator' pattern.
    Provides access to other objects attributes.
    Also its Singleton and i'm not sure if you're ok with that.
    '''

    def __new__(cls, obj=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(cls, cls).__new__(cls)
        return cls.instance

    def __init__(self):

        self.objects = {}

    def __call__(self, obj):
        self.objects[obj.name] = obj
        return self

    def __str__(self):
        return 'Mediator. Watch objects: [{}]'.format(', '.join(self.objects.keys()))

    def _get_value(self, name):
        for obj in self.objects:
            try:
                return obj[name]
            except KeyError:
                continue

        raise AttributeError('Name {} was not found in objects'.format(name))

    def get(self, key):
        try:
            obj_name, name = key.split('.')
        except IndexError:
            name = key
        else:
            return self.objects[obj_name][name]

        return self._get_value(name)


import math
import builtins
modules = math, builtins


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

    @staticmethod
    def _unidecode(value):
        return unidecode.unidecode(value.lower().replace(' ', '_'))

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

    @classmethod
    def parse_structure(cls, structure):

        structure = cls._unidecode(structure)
        try:
            structure = json.loads(structure)
        except ValueError:
            print('Bad structure. Exiting program')
            sys.exit()

        return structure


class CalculableObject(OrderedDict):

    def __init__(self, name, args, parser, mediator):
        super().__init__()

        self.name = name
        self.mediator = mediator(self)
        self.calculations = []

        for each in args:
            self[each['name']] = 0
            calculation = each.get('calculation')
            if calculation:
                self.calculations.append(
                    parser.parse_calculation_string(each['name'], calculation))

        self.calculations = '\n'.join(self.calculations)

    def _set(self, name, value):
        if self.get(name) is None:
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

    print(mediator)


def test_json_to_structure():
    import pprint
    parser = Parser()

    parsed_structure = parser.parse_structure(STRUCTURE)
    pprint.pprint(parsed_structure)


# test_calc_obj()
test_json_to_structure()

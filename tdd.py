import pprint
import sys
import re
import json
from collections import OrderedDict

import unidecode


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

    property_re = re.compile(r'[^\W\d]+\.?[\w\_\'"]*', re.UNICODE)
    module_str = '{}.{}'
    get_str = 'self._get("{}")'
    self_str = 'self._set("{}", {})'

    @staticmethod
    def _unidecode(value):
        return unidecode.unidecode(value.lower().replace(' ', ''))

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

    def __str__(self):
        return '{}: [{}]'.format(self.name, ', '.join(self.keys()))

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
        try:
            exec(self.calculations)
        except (ZeroDivisionError):
            pass


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

# class Client(Base):

#     __tablename__ = 'client'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False, default='')
#     surname = Column(String, nullable=False, default='')
#     patronymic = Column(String, nullable=False, default='')
#     date_of_birth = Column(Date)
#     hr = Column(SmallInteger, nullable=False, default=0)
#     height = Column(SmallInteger, nullable=False, default=0)
#     weight = Column(SmallInteger, nullable=False, default=0)
#     examined = Column(Date, nullable=False, default=datetime.datetime.now)
#     user = Column(ForeignKey('user.id'), nullable=False)
#     sent_by = Column(String, nullable=False, default='')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, String, Float,
                        ForeignKey, Date, SmallInteger,
                        Text)
DATABASE = 'data.db'
Base = declarative_base()
engine = create_engine('sqlite:///{}'.format(DATABASE), echo=True)
SESSION = sessionmaker()(bind=engine)


def test_json_to_structure():
    parser = Parser()

    parsed_structure = parser.parse_structure(STRUCTURE)
    pprint.pprint(parsed_structure)


def test_json_to_objs():
    parser = Parser()
    model_factory = ModelFactory()
    parsed_structure = parser.parse_structure(STRUCTURE)

    for item in parsed_structure:
        if item.get('db'):
            db_class = model_factory.get_model(item)
            print(db_class)
    Base.metadata.create_all(engine)

    #     c = CalculableObject(item['name'], item['args'], parser, Mediator())
    #     print(c.name)
    #     print(c.calculations_str())
    #     c.calculate()
    # c = CalculableObject(parsed_structure[1]['name'], parsed_structure[1]['args'], parser, Mediator())
    # k = CalculableObject(parsed_structure[0]['name'], parsed_structure[0]['args'], parser, Mediator())

    # print(c.calculations)
    # c._set('ksrlzh', 10)
    # c._set('kdrlzh', 10)
    # c.calculate()
    # print(c._get('kdo'))

# test_calc_obj()
# test_json_to_structure()
# test_json_to_objs()
# kdr = 10
# a = 7/(2.4+kdr)*kdr**3
#  print(a)


a = {}

for x in ({'a': 1}, {'b': 2}):
    a.update(x)

print(a)

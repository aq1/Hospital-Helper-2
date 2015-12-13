# -*- coding: UTF-8 -*-

import sys
import re
import json
import math
import builtins
import collections
from collections import defaultdict

import unidecode

from model import exceptions, db


class AllowedModule(list):

    excluded_attr = ('exec', 'eval')

    def __init__(self, module):
        self.name = module.__name__
        super().__init__(
            [attr for attr in dir(module) if attr not in self.excluded_attr])


MODULES = math, builtins
ALLOWED_MODULES = [AllowedModule(module) for module in MODULES]


class Parser:

    """
    Used to parse structure and calculation strings
    """

    property_re = re.compile(r'[^\W\d]+\.?[\w\_\'"]*', re.UNICODE)
    module_str = '{}.{}'
    get_str = 'self._get("{}")'
    self_str = 'self._set("{}", {})'

    @staticmethod
    def unidecode(value):
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

        structure = cls.unidecode(structure)

        try:
            structure = json.loads(structure)
        except ValueError:
            raise exceptions.BadStructure()
            sys.exit()

        return structure


class Mediator:

    """
    Sort of implementation of 'Mediator' pattern.
    Provides access to other objects attributes.
    Also its Singleton and i'm not sure if you're ok with that.
    """

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


class CalculableObject(collections.OrderedDict):

    def __init__(self, name, verbose_name, group, args, parser, mediator, model=None):
        super().__init__()

        self.name = name
        self.verbose_name = verbose_name
        self.group = group
        self.mediator = mediator(self)
        self.model = model
        self.calculations = []
        self.template = None

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

    def get_verbose_name(self):
        return _(self.verbose_name)

    def calculate(self):
        try:
            exec(self.calculations)
        except (ZeroDivisionError):
            pass

    def for_template(self):
        out = {
            self.name: defaultdict(str)
        }

        for key, value in self.items():
            out[self.name][key] = value
        return out


class ObjectFactory:

    model_factory = db.ModelFactory()

    @classmethod
    def get_object(cls, info):

        if info.get('db'):
            model = cls.model_factory.get_model(info)

        return CalculableObject(name=info['name'],
                                verbose_name=info.get('verbose_name', info['name']),
                                args=info['args'],
                                group=info.get('group', info['name']),
                                parser=Parser(),
                                mediator=Mediator(),
                                model=model)

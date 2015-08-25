# -*- coding: UTF-8 -*-

import unittest
import json

from app.logic.json_to_obj import JsonToObj
from app.logic.organ import Organ


class TestJsonToObj(unittest.TestCase):

    def setUp(self):
        self.klass = Organ
        self.json_to_obj = JsonToObj(Organ)

        with open('structure.json', 'r', encoding='utf8') as f:
            self.json = json.loads(f.read())

    def test_object_creation(self):
        args = {'name': 'TestOrgan',
                'args': [['arg0'],
                         ['arg1', 'arg0 + hello'],
                         ['arg2', 'arg1 + arg1']]
                }

        obj = JsonToObj(self.klass, args).create_obj()
        self.assertIsInstance(obj, Organ)

    def test_str_to_expr(self):
        string = 'arg + hello - 4'
        indexes = {'arg': 0}
        out = self.json_to_obj._str_to_expr(string=string, indexes=indexes)

        self.assertEqual(
            out, 'self.arg + self._get_value_from_mediator("hello") - 4')

    def test_repr(self):
        self.assertEqual(
            self.json_to_obj.__repr__(), self.json_to_obj.__class__.__name__)

    def test_real_json(self):
        organs = self.json['organs']
        for organ in organs:
            obj = JsonToObj(self.klass, organ).create_obj()
            self.assertIn(organ['args'][0][0], obj.__dict__)
            self.assertEqual(len(obj.args), len(organ['args']))

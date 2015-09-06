# -*- coding: UTF-8 -*-

import json

from app.tests.test_calculable_object import TestCalculableObject
from app.logic import CalculableObject
from app.data import Data


with open(r'app\tests\structure.json', 'r', encoding="utf8") as f:
    f = json.load(f)
    for x in f:
        CalculableObject(x['name'], x['args'])
        # print(CalculableObject(x['name'], x['args']))
        # print('=' * 10)

# a = TestCalculableObject()
# a.setUp()
d = Data()
d.assemble_data()

# a.test_calculation()

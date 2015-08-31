# -*- coding: UTF-8 -*-

# import json

# from app.logic import AbstractObject


# with open(r'app\tests\structure.json', 'r', encoding="utf8") as f:
#     f = json.load(f)
#     for x in f:
#         print(AbstractObject(x['name'], x['args']))
#         print('=' * 10)


from app.tests.test_calculable_object import TestCalculableObject
a = TestCalculableObject()
a.setUp()
a.test_calculation()

print(str(a.object_b))

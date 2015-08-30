# -*- coding: UTF-8 -*-

# import importlib
import math
import builtins

modules = math, builtins


class AllowedModule(list):

    excluded_attr = ('exec', 'eval')

    def __init__(self, module):
        self.name = module.__name__
        super().__init__(
            [attr for attr in dir(module) if attr not in self.excluded_attr])


# for module in modules:
#     print('hello\n\n\n\n\n\n')
#     globals()[module] = importlib.import_module(module)

ALLOWED_MODULES = [AllowedModule(module) for module in modules]

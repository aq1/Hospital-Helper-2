# -*- coding: UTF-8 -*-

import re
from . import ALLOWED_MODULES


PROPERTY_RE = re.compile(r'[^\W\d]+[\w\-_]*', re.UNICODE)


class Parser(object):

    module_str = '{}.{}'
    mediator_str = 'self._get_from_mediator("{}")'
    self_str = 'self["{}"]'

    def str_to_calculation(self, key, string):
        # Mew. Too complicated i guess

        out = []
        i = 0

        for match in PROPERTY_RE.finditer(string):
            begin, end = match.span()
            group = match.group()

            for module in ALLOWED_MODULES:
                if group in module:
                    group = self.module_str.format(module.name, group)
                    break
            else:
                group = self._unidecode(group)
                try:
                    self[group]
                except KeyError:
                    group = self.mediator_str.format(group)
                else:
                    group = self.self_str.format(group)

            out.append(''.join((string[i:begin], group)))
            i = end
        else:
            out.append(string[i:])

        expr = ''.join([chunk for chunk in out])
        return '{} = {}'.format(self.self_str.format(key), expr)

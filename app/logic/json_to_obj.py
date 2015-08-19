# -*- coding: UTF-8 -*-


import re


class JsonToObj(object):

    '''
    Translates json object to a 'klass' objects.

    It's meant that json is generated initially by programmer
    and can be edited by user, so there has to be an automatic
    process that creates objects.
    '''

    def __init__(self, klass, args=None):

        if args:
            assert isinstance(args, dict)
            assert args.get('name', None) and args.get('args', None)

        self.re = re.compile(r'[a-zA-Z]+[a-zA-Z0-9\-_]*')
        self.klass = klass
        self.args = args

    def _str_to_expr(self, string, indexes):
        # Mew. Too complicated i guess
        i = 0
        out = []

        for match in self.re.finditer(string):
            begin, end = match.span()
            group = match.group()
            try:
                indexes[group]
                replacement = 'self.{}'.format(group)
            except KeyError:
                replacement = 'self._get_value_from_mediator("{}")'.format(group)

            out.append(string[i:begin])
            out.append(replacement)
            i = end

        out.append(string[i:])
        return ''.join(out)

    def _convert_args(self, arg_list):
        out = []

        indexes = {arg[0]: i for (i, arg) in enumerate(arg_list)}

        for each in arg_list:
            try:
                arg, expr = each
            except ValueError:
                # No second argument == value will not be calculated
                out.append(each)
                continue

            exec_str = 'self.{} = {}'.format(arg, self._str_to_expr(expr, indexes))
            out.append([arg, exec_str])

        return out

    def create_obj(self, klass=None, args=None):
        if not klass:
            klass = self.klass
        if not args:
            args = self.args

        name = args['name']
        args = self._convert_args(args['args'])

        return klass(name, args)

    def __repr__(self):
        return self.__class__.__name__

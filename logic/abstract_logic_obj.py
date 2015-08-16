# -*- coding: UTF-8 -*-


class AbstractObject(object):

    def __init__(self, name, args):
        self.name = name
        self.args = args

        for arg in args:
            self.__dict__[arg] = 0

    def get(self, key):
        return self.__dict__[key]

    def __repr__(self):
        args = []
        for i, each in enumerate(self.args):
            try:
                arg = '{}={}'.format(each[0], each[1])
            except IndexError:
                arg = each[0]

            args.append('{}: {}'.format(i, arg))

        return '{}:\n{}'.format(self.name, ';\n'.join(args))

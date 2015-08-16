# -*- coding: UTF-8 -*-


class Mediator(object):

    def __init__(self, obj_list=None):
        self.obj_list = obj_list or []

    def get_attr(self, key):
        for obj in self.obj_list:
            try:
                return obj.get(key)
            except AttributeError:
                continue

        else:
            raise AttributeError('{} was not found in objects'.format(key))

    def 
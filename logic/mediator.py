# -*- coding: UTF-8 -*-


class Mediator(object):

    '''
    Sort of implementation of 'Mediator' pattern.
    Provides access to other objects attributes.
    Also its Singleton and i'm not sure if you're ok with that.
    '''

    obj_dict = {}

    def __new__(cls, obj=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(cls, cls).__new__(cls)
        return cls.instance

    def __init__(self, obj=None):
        self.add_obj(obj)

    def add_obj(self, obj):
        for attr in ('name', 'get'):
            assert hasattr(obj, attr)

        self.obj_dict[obj.name] = obj

    def get_attr(self, key):
        for _, obj in self.obj_dict.items():
            try:
                return obj.get(key)
            except KeyError:
                continue
        else:
            raise AttributeError('Attribute "{}" was not found in objects'.format(key))

    def get_attr_from_class(self, class_name, key):
        return self.obj_dict[class_name].get(key)

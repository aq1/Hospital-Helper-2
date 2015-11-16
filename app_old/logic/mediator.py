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
        if obj is not None:
            self.add_obj(obj)

    def __iter__(self):
        return iter(self.obj_dict.values())

    def add_obj(self, obj):
        for attr in ('name', 'get_value'):
            assert hasattr(obj, attr)

        self.obj_dict[obj.name] = obj

    def _get_by_key(self, key):
        for _, obj in self.obj_dict.items():
            try:
                return obj.get_value(key)
            except KeyError:
                continue
        else:
            raise AttributeError('Attribute "{}" was not found in objects'.format(key))

    def _get_by_name_and_key(self, name, key):
        return self.obj_dict[name][key]

    def get(self, key):
        dot = key.find('.')
        if dot != -1:
            return self._get_by_name_and_key(key[:dot], key[dot+1:])
        else:
            return self._get_by_key(key)

    def get_attr_from_class(self, class_name, key):
        return self.obj_dict[class_name].get(key)

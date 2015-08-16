class A:

    dict_ = {}

    def __init__(self, arg_list):
        for x in arg_list:
            self.__dict__[x] = 0

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value


a = A(['hello', 0, 'man'])
print(a.hello)
print(a.dict_)
a.dict_['123'] = 123123
print(a.dict_)
b = A([])
b.dict_['123'] = 'asdd'
print(a.dict_)
print(b.dict_)

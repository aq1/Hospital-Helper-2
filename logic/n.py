class A:

    def __init__(self, arg_list):
        for x in arg_list:
            self.__dict__[x] = 0


a = A(['hello', 'there', 'man'])

print(a.hello)

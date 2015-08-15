# -*- coding: UTF-8 -*-

from json_to_obj import JsonToObj


class Patient(object):

    def __init__(self, name, data):
        self.name = Patient
        self.data = data

    def __repr__(self):
        return 'Patient'


class TestProperty(object):

    def __init__(self, x):
        # self.x = x
        pass

    @property
    def x(self):
        return 42

    @x.setter
    def x(self, x):
        raise AttributeError('This attribute is calculated only')
        return 42

if __name__ == '__main__':
    patient_args = {'name': 'Patient',
                    'args': [['doctor'],
                             ['surname'],
                             ['patronymic'],
                             ['name'],
                             ['hr'],
                             ['weight'],
                             ['height'],
                             ['date'],
                             ['year_of_birth'],
                             ['bsa', '(weight + height) / age'],
                             ['sent_by']]}

    patient = JsonToObj(klass=Patient, data=patient_args).create_obj()
    print(patient)

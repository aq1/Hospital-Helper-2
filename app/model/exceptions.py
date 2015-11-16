# -*- coding: UTF-8 -*-


class BadStructure(Exception):

    def __str__(self):
        return 'Bad Structure'


class NonUniqueObjectNames(BadStructure):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Non-unique name found in structure: {}'.format(self.name)

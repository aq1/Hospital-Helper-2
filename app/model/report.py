# -*- coding: UTF-8 -*-

from model import db


class Report:

    def __init__(self, items):

        self.items = []

        for item in items:
            if item.template and any(item.values()):
                self.items.append(item)

# -*- coding: UTF-8 -*-

from . import SESSION, Client
from ..logic import Mediator


class Data(object):

    def __init__(self, mediator=Mediator()):
        self.mediator = mediator
        self.data = {}

    def assemble_data(self):

        for obj in self.mediator:
            self.data[obj.name] = obj.get_items()

    def export_client_to_db(self):

        client = self.data.get('client', None)

        if not client:
            return

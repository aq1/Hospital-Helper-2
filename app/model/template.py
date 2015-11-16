# -*- coding: UTF-8 -*-

from model import db


class Report:

    def __init__(self, organ, name):
        self.template = db.SESSION.query(db.Template).filter(
            db.Item.name == 'serdtse').first()

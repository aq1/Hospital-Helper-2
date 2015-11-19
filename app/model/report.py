# -*- coding: UTF-8 -*-

from model import db


class Report:

    def __init__(self, items):

        self.items = []
        self.templates = []

        for item in items:
            if item.template and any(item.values()):
                self.items.append(item)

    def get_templates(self):

        for item in self.items:
            db_item = db.SESSION.query(db.Item).filter(
                db.Item.name == item.name).first()
            template = db.SESSION.query(db.Template).filter(
                db.Template.item == db_item.id, db.Template.name == item.template).first()

            self._add_template()
            self.templates.append({
                'item': item,
                'group': db_item.group,
                'template': template
            })

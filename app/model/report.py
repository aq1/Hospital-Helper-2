# -*- coding: UTF-8 -*-

from model import db


class Report:

    def __init__(self, items):

        self.items = []

        for item in items:
            if item.template and any(item.values()):
                self.items.append(item)

    def get_templates(self):

        kwargs = []
        for item in self.items:
            db_item = db.SESSION.query(db.Item).filter(
                db.Item.name == item.name).first()
            template = db.SESSION.query(db.Template).filter(
                db.Template.item == db_item.id, db.Template.name == item.template).first()

            kwargs.append({
                'item': db_item.id,
                'group': db_item.group,
                'template': template
            })
            print(kwargs[-1])
        # kwargs = [{'item': ,
        #            'group': db.SESSION.query(db.Group).filter()
        #            'template': i.template}
        #           for i in self.items]

        # print(kwargs)

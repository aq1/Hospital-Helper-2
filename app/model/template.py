import re
import json
from collections import defaultdict

from app.model import db, exceptions


class Template:

    def __init__(self, pk=None, item=None, items=None, name=None, body=None, conclusion=None):

        """
        Parameter items is needed
        because template for one particular item
        can contain keywords from another items.
        And parameter item is needed too,
        because template needs to know for what item it is saved.
        """

        self.pk = pk
        self.item = item
        self.items = items
        self.name = name
        self.body = body
        self.conclusion = conclusion

    def __str__(self):
        return 'Template "{}"'.format(self.name)

    def save(self, force=False):

        if not (self.item and self.name):
            raise exceptions.CannotSaveTemplate

        if not (self.body or self.conclusion):
            raise exceptions.NeedBodyOrConclusion

        if self.pk:
            template = db.SESSION.query(db.Template).get(self.pk)
        else:
            template = db.Template()

        template.item_id = self.item.id
        template.name = self.name
        template.body = self.body
        template.conclusion = self.conclusion
        template.save()
        self.pk = template.id

    def get_translated_body(self, reverse=False):
        """
        This is bad function.
        """
        
        regex = {}
        translation = {}

        if reverse:
            for each in self.items:
                for k in each.keys():
                    regex[r'{%s.%s}' % (_(each.name), _(k))] = r'{%s[%s]}' % (each.name, k)
                    translation = regex
        else:
            for each in self.items:
                for k in each.keys():
                    regex[r'{%s\[%s\]}' % (each.name, k)] = r'{%s.%s}' % (_(each.name), _(k))
                    translation[r'{%s[%s]}' % (each.name, k)] = r'{%s.%s}' % (_(each.name), _(k))

        pattern = re.compile(r'(' + '|'.join(regex.keys()) + r')')
        return pattern.sub(lambda x: translation[x.group()], self.body)

    def render_and_save(self):
        self.body = self.get_translated_body(reverse=True)
        self.save()

    # def to_dict(self):


    @classmethod
    def get_from_db(cls, item, items, name):

        template = db.SESSION.query(db.Template).filter(
            db.Template.item_id == item.id, db.Template.name == name).first()

        return cls(pk=template.id,
                   item=item,
                   items=items,
                   name=name,
                   body=template.body,
                   conclusion=template.conclusion)

    @classmethod
    def get_all(cls):

        result = defaultdict(list)
        templates = db.SESSION.query(db.Template).all()

        for each in templates:
            result[each.item.id].append(each)

        return result

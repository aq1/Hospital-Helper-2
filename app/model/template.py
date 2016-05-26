import re
from collections import defaultdict

from model import db, exceptions, localization


class Template:

    def __init__(self, pk=None, item=None, name=None, body=None, conclusion=None):

        self.pk = pk
        self.item = item
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
        translation_map = localization.Localization.get_translation_map(self.item.keys())
        if reverse:
            regex = {r'{%s}' % v: r'{%s[%s]}' % (self.item.name, k) for (k, v) in translation_map.items()}
            translation = regex
        else:
            regex = {}
            translation = {}
            for (k, v) in translation_map.items():
                # God dammit.
                regex[r'{%s\[%s\]}' % (self.item.name, k)] = r'{%s}' % v
                translation[r'{%s[%s]}' % (self.item.name, k)] = r'{%s}' % v

        pattern = re.compile(r'(' + '|'.join(regex.keys()) + r')')
        return pattern.sub(lambda x: translation[x.group()], self.body)

    def render_and_save(self):
        self.body = self.get_translated_body(reverse=True)
        self.save()

    @classmethod
    def get_from_db(cls, item, name):

        template = db.SESSION.query(db.Template).filter(
            db.Template.item_id == item.id, db.Template.name == name).first()

        return cls(pk=template.id,
                   item=item,
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

from collections import defaultdict

from model import db, exceptions


class Template:

    def __init__(self, item=None, name=None, body=None, conclusion=None):

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

        template, created = db.Template.get_or_create(item=self.item, name=self.name)

        if not created and not force:
            raise exceptions.TemplateAlreadyExists

        template.body = self.body
        template.conclusion = self.conclusion
        db.SESSION.add(template)
        db.SESSION.flush()

    @classmethod
    def get_from_db(cls, item, name):

        template = db.SESSION.query(db.Template).filter(
            db.Template.item == item, db.Template.name == name).first()

        return cls(item=item,
                   name=name,
                   body=template.body,
                   conclusion=template.conclusion)

    @classmethod
    def get_list(cls):

        result = defaultdict(list)
        templates = db.SESSION.query(db.Template).all()

        for each in templates:
            result[each.item.id].append(each)

        return result

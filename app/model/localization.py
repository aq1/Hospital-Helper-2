# -*- coding: UTF-8 -*-

import json

from model import db, logic, exceptions
import options


class Localization:

    __translation = {}

    @classmethod
    def install(cls, lang):

        if lang not in [c.name for c in db.Translation.__table__.columns]:
            raise exceptions.NoSuchTranslation

        strings = db.SESSION.query(db.Translation).all()

        for s in strings:
            transl = getattr(s, lang)
            cls.__translation[s.sys] = transl

        import builtins
        builtins.__dict__['_'] = cls.get_text

    @classmethod
    def get_text(cls, text):
        try:
            return cls.__translation[text]
        except KeyError:
            return text


def add_system_label(label):

    t, _ = db.Translation.get_or_create(sys=logic.Parser.unidecode(label),
                                        defaults={
        'ru': label
    })

    db.SESSION.add(t)


def create_init_translation():

    structure = json.loads(db.SESSION.query(db.KeyValue).filter(
        db.KeyValue.key == options.STRUCTURE_KEY).first().value)

    for item in structure:
        for arg in item['args']:
            add_system_label(arg['name'])

        if item.get('group'):
            add_system_label(item['group'])

        add_system_label(item['name'])

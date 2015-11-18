# -*- coding: UTF-8 -*-

import datetime

import slugify

from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, String, Float,
                        ForeignKey, Date, SmallInteger,
                        Text)

import options


Base = declarative_base()
engine = create_engine('sqlite:///{}'.format(options.DATABASE), echo=False)
SESSION = sessionmaker()(bind=engine, autocommit=True, expire_on_commit=False)


class Model:

    @classmethod
    def get_or_create(cls, defaults=None, instant_flush=False, **kwargs):
        inst = SESSION.query(cls).filter_by(**kwargs).first()

        if inst:
            return inst, False

        if defaults:
            kwargs.update(defaults)

        inst = cls(**kwargs)
        SESSION.add(inst)

        if instant_flush:
            SESSION.flush()

        return inst, True


class Client(Base, Model):

    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='')
    surname = Column(String, nullable=False, default='')
    patronymic = Column(String, nullable=False, default='')
    date_of_birth = Column(Date)
    hr = Column(SmallInteger, nullable=False, default=0)
    height = Column(SmallInteger, nullable=False, default=0)
    weight = Column(SmallInteger, nullable=False, default=0)
    examined = Column(Date, nullable=False, default=datetime.datetime.now)
    doctor = Column(ForeignKey('doctor.id'), nullable=False)
    sent_by = Column(String, nullable=False, default='')


class Doctor(Base, Model):

    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='')
    surname = Column(String, nullable=False, default='')
    patronymic = Column(String, nullable=False, default='')
    hospital = ForeignKey('hospital.id')


class Hospital(Base, Model):

    __tablename__ = 'hospital'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    header = Column(Text, nullable=False, default='')


class Report(Base, Model):

    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    client = Column(ForeignKey('client.id'))
    path = Column(String, nullable=False)
    template = Column(ForeignKey('template.id'))


class Group(Base, Model):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Item(Base, Model):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    group = Column(ForeignKey('group.id'))
    name = Column(String, nullable=False)


class Template(Base, Model):

    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    item = Column(ForeignKey('item.id'))
    name = Column(String, nullable=False, default='')
    body = Column(Text, nullable=False, default='')
    conclusion = Column(Text, nullable=False, default='')


class KeyValue(Base, Model):

    __tablename__ = 'key_value'

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


class ModelFactory:

    def __init__(self):
        self.default_type = 'float'

        self.field_type_map = {
            'str': String,
            'float': Float,
            'int': Integer,
            'text': Text,
        }

    def get_model(self, item):
        fields = {}
        fields['__tablename__'] = slugify.slugify(item['name'])
        fields['id'] = Column(Integer, primary_key=True)
        for f in item['args']:
            field_type = self.field_type_map[f.get('type', self.default_type)]
            fields[f['name']] = Column(field_type,
                                       nullable=False,
                                       default='')

        for rel in item.get('relations', []):
            fields[rel] = Column(
                ForeignKey('{}.id'.format(rel)), nullable=False)

        group, _ = Group.get_or_create(name=item.get('group', item['name']),
                                       instant_flush=True)
        Item.get_or_create(name=item['name'], group=group.id)

        try:
            return type('{}Model'.format(item['name']), (Base, ), fields)
        except exc.InvalidRequestError as e:
            print(e)
            return


def create_db():
    Base.metadata.create_all(engine)


create_db()

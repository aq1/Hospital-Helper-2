# -*- coding: UTF-8 -*-

import datetime

import slugify

from sqlalchemy import exc, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship
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
    sent_by = Column(String, nullable=False, default='')

    doctor_id = Column(ForeignKey('doctor.id'), nullable=False)
    doctor = relationship('Doctor', backref='client')


class Doctor(Base, Model):

    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    hospital_id = Column(ForeignKey('hospital.id'))
    hospital = relationship('Hospital', backref='doctor')

    name = Column(String, nullable=False, default='')
    surname = Column(String, nullable=False, default='')
    patronymic = Column(String, nullable=False, default='')


class Hospital(Base, Model):

    __tablename__ = 'hospital'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    header = Column(Text, nullable=False, default='')

    __table_args__ = tuple(UniqueConstraint('name'))


class Report(Base, Model):

    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)

    client_id = Column(ForeignKey('client.id'))
    template_id = Column(ForeignKey('template.id'))

    client = relationship('Client', backref='report')
    template = relationship('Template', backref='report')


class Group(Base, Model):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    __table_args__ = tuple(UniqueConstraint('name'))


class Item(Base, Model):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(ForeignKey('group.id'))
    group = relationship('Group', backref='item')

    __table_args__ = tuple(UniqueConstraint('group', 'name'))

    def __str__(self):
        return '{} {}'.format(self.group, self.name)


class Template(Base, Model):

    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='')
    body = Column(Text, nullable=False, default='')
    conclusion = Column(Text, nullable=False, default='')

    item_id = Column(ForeignKey('item.id'))
    item = relationship('Item', backref='template')

    __table_args__ = tuple(UniqueConstraint('item', 'name'))


class KeyValue(Base, Model):

    __tablename__ = 'key_value'

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)

    __table_args__ = tuple(UniqueConstraint('key', 'value'))


class Translation(Base, Model):

    __tablename__ = 'translation'

    sys = Column(String, primary_key=True)
    ru = Column(String, nullable=False)
    en = Column(String, nullable=True)


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

        try:
            return type('{}Model'.format(item['name']), (Base, ), fields)
        except exc.InvalidRequestError as e:
            print(e)
            return


def create_db():
    Base.metadata.create_all(engine)


create_db()

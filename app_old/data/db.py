# -*- coding: UTF-8 -*-

import os
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, Date, SmallInteger,
                        Text)

DATABASE = 'data.db'
Base = declarative_base()
engine = create_engine('sqlite:///{}'.format(DATABASE), echo=False)
SESSION = sessionmaker()(bind=engine)


class Client(Base):

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


class Doctor(Base):

    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='')
    surname = Column(String, nullable=False, default='')
    patronymic = Column(String, nullable=False, default='')
    hospital = ForeignKey('hospital.id')


class Hospital(Base):

    __tablename__ = 'hospital'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    header = Column(Text, nullable=False, default='')


class Report(Base):

    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    client = Column(ForeignKey('client.id'))
    path = Column(String, nullable=False)
    template = Column(ForeignKey('template.id'))


class Organ(Base):

    __tablename__ = 'organ'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Template(Base):

    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    organ = Column(ForeignKey('organ.id'))
    body = Column(Text, nullable=False, default='')
    conclusion = Column(Text, nullable=False, default='')


class Settings(Base):

    __tablename__ = 'settings'
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


if not os.path.exists(DATABASE):
    Base.metadata.create_all(engine)

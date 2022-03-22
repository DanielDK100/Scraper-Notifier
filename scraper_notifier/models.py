# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)
from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    # return create_engine(get_project_settings().get('CONNECTION_STRING'))
    return True


def create_table(engine):
    # DeclarativeBase.metadata.create_all(engine)
    return True


class ReservationDB(DeclarativeBase):
    __tablename__ = 'laundry_reservations'

    id = Column(Integer, primary_key=True)
    reserved_at = Column('reserved_at', DateTime)
    group = Column('group', String(100))
    ordered_at = Column('ordered_at', DateTime)
    notified_at = Column('notified_at', DateTime)

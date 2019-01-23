#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, relationship

from . import settings

eng = create_engine(settings.DATABASE_URI)

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'Currencies'

    Value = Column(String, primary_key=True)

class Account(Base):
    __tablename__ = "Accounts"

    Name = Column(String, primary_key=True)
    Transactions = relationship('Transaction')
    Currency = Column(Integer, ForeignKey(Currency.Value))

class Transaction(Base):
    __tablename__ = "Transactions"

    Id = Column(Integer, primary_key=True)
    Account = Column(Integer, ForeignKey(Account.Name))
    Amount = Column(Float)

if __name__ == '__main__':
    Base.metadata.bind = eng
    Base.metadata.create_all()

    Session = sessionmaker(bind=eng)
    session = Session()

    session.add_all([
        Currency(Value='USD'),
        Currency(Value='GBP'),
        Currency(Value='EUR'),
        Currency(Value='JPY'),
        Currency(Value='RUB'),
    ])
    session.commit()
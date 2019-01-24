#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import datetime

from sqlalchemy import event, and_
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, relationship

from . import settings
from .common import get_forex
from .exceptions import MoneyLaunderingException

eng = create_engine(settings.DATABASE_URI)

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'Currencies'

    Value = Column(String, primary_key=True)
    Accounts = relationship('Account')

class Account(Base):
    __tablename__ = "Accounts"

    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Transactions = relationship('Transaction')
    Currency = Column(String, ForeignKey(Currency.Value))

class Transaction(Base):
    __tablename__ = "Transactions"

    Id = Column(Integer, primary_key=True)
    Account = Column(Integer, ForeignKey(Account.Id))
    Amount = Column(Float)
    Date = Column(Date, default=datetime.datetime.now(settings.TIMEZONE).date())

@event.listens_for(Transaction, 'before_insert')
def receive_before_insert(mapper, connection, target):
    '''
    Money Laundering Clause
    '''
    Session = sessionmaker()
    s = Session(bind=connection)
    target_account = s.query(Account).filter_by(Id=target.Account).first()
    accounts = s.query(Account).filter_by(Name=target_account.Name)

    currencies = [c.Value for c in s.query(Currency).all()]
    if 'EUR' in currencies:
        currencies.pop(currencies.index('EUR')) # because this is a base currency
    logging.debug(currencies)
    forex = get_forex(currencies)
    rates = forex['rates']

    today = datetime.datetime.now(settings.TIMEZONE)
    last_5_days = today - datetime.timedelta(days=5)
    total_money = 0

    for account in accounts:
        transactions = s.query(Transaction).filter(and_(Transaction.Account == account.Id,
                                                        Transaction.Date >= last_5_days))
        for transaction in transactions:
            if account.Currency == settings.DEFAULT_CURRENCY:
                total_money += transaction.Amount
            else:
                total_money += transaction.Amount * rates[account.Currency]

    if (total_money + target.Amount) > 10000:
        raise MoneyLaunderingException('10,000 %s limit exceeded' % settings.DEFAULT_CURRENCY)

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

    logging.info('Database successfully created at %s', settings.DATABASE_URI)

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ... import settings
from ...db import Currency, Account
from ...exceptions import MoneyLaunderingException

class Base:

    status = 0

    def __init__(self, json_obj):
        self.json_obj = json_obj
        eng = create_engine(settings.DATABASE_URI)
        Session = sessionmaker(bind=eng)
        self.session = Session()

    def action(self, action_class, **kwargs):
        try:
            return action_class(**kwargs)
        except MoneyLaunderingException as e:
            self.status = e.msg

    def get_currency(self):
        ccy = self.json_obj.get('ccy', settings.DEFAULT_CURRENCY).upper()
        currency = self.session.query(Currency) \
                               .filter_by(Value=ccy) \
                               .first()
        if not currency:
            raise 'Invalid Currency'
        return currency

    def get_or_create_account(self, name):
        currency = self.get_currency()
        account = self.session.query(Account) \
                              .filter_by(Name=name, Currency=currency.Value) \
                              .first()
        if not account:
            account = Account(Name=name, Currency=currency.Value)
            self.session.add(account)
            self.session.commit()

        account = self.session.query(Account) \
                              .filter_by(Name=name, Currency=currency.Value) \
                              .first()
        return account

    def toJSON(self):
        return json.dumps('{status: %s}' % self.status)

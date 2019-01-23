from ...db import Currency, Account, Transaction
from ... import settings
from .base import Base

class Deposit(Base):

    def __init__(self, json_obj):
        super(Deposit, self).__init__(json_obj) # initiates self.session

        ccy = json_obj.get('ccy', settings.DEFAULT_CURRENCY)
        currency = self.session.query(Currency).filter_by(Value=ccy).first()
        if not currency:
            raise 'Invalid Currency'

        name = json_obj.get('account')
        account = self.session.query(Account).filter_by(Name=name, Currency=currency).first()
        if not account:
            account = Account(Name=name, Currency=currency)
            self.session.add(account)

        # FIXME: verify if money is under threshold of money laundering laws
        amount = json_obj.get('amt')
        money = Transaction(Account=account, Amount=amount)
        self.session.add(money)

        self.session.commit()

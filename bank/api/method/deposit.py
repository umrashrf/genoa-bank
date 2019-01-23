from ...db import Account, Transaction
from .base import Base


class Deposit(Base):

    def __init__(self, json_obj):
        super(Deposit, self).__init__(json_obj) # initiates self.session

        currency = self.get_currency()

        name = json_obj.get('account')
        account = self.session.query(Account) \
                              .filter_by(Name=name, Currency=currency.Value) \
                              .first()
        if not account:
            account = Account(Name=name, Currency=currency.Value)
            self.session.add(account)

        # FIXME: verify if money is under threshold of money laundering laws
        amount = json_obj.get('amt')
        money = Transaction(Account=account.Name, Amount=amount)
        self.session.add(money)

        self.session.commit()

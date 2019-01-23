from ...db import Account, Transaction
from .base import Base


class Transfer(Base):

    def __init__(self, json_obj):
        super(Transfer, self).__init__(json_obj) # initiates self.session

        currency = self.get_currency()

        from_name = json_obj.get('from_account')
        from_account = self.get_account(from_name, currency=currency.Value)

        to_name = json_obj.get('to_account')
        to_account = self.get_account(to_name, currency=currency.Value)

        money = json_obj.get('amt')
        withdraw = Transaction(Account=from_account.Name, Amount=-money)
        deposit = Transaction(Account=to_account.Name, Amount=money)
        self.session.add_all([withdraw, deposit])

        self.session.commit()

    def get_account(self, name, currency):
        account = self.session.query(Account).filter_by(Name=name, Currency=currency).first()
        if not account:
            account = Account(Name=name, Currency=currency)
            self.session.add(account)
        return account

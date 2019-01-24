from ...db import Transaction
from .base import Base


class Deposit(Base):

    def __init__(self, json_obj):
        super(Deposit, self).__init__(json_obj) # initiates self.session

        name = json_obj.get('account')
        account = self.get_or_create_account(name)

        # FIXME: verify if money is under threshold of money laundering laws
        amount = json_obj.get('amt')
        money = Transaction(Account=account.Id, Amount=amount)
        self.session.add(money)
        self.session.commit()

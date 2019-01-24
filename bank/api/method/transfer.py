from ...db import Transaction
from .base import Base


class Transfer(Base):

    def __init__(self, json_obj):
        super(Transfer, self).__init__(json_obj) # initiates self.session

        from_name = json_obj.get('from_account')
        from_account = self.get_or_create_account(from_name)

        to_name = json_obj.get('to_account')
        to_account = self.get_or_create_account(to_name)

        money = json_obj.get('amt')
        withdraw = self.action(Transaction, Account=from_account.Id, Amount=-money)
        deposit = self.action(Transaction, Account=to_account.Id, Amount=money)
        self.session.add_all([withdraw, deposit])

        self.session.commit()

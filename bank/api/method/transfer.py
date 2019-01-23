from ...db import Account,  Transaction
from .base import Base


class Transfer(Base):

    def __init__(self, json_obj):
        super(Transfer, self).__init__(json_obj) # initiates self.session

        name = json_obj.get('account')
        account = self.session.query(Account).filter_by(Name=name).first()
        if not account:
            account = Account(Name=name)
            self.session.add(account)

        money = json_obj.get('amt')
        withdraw = Transaction(To=account, Amount=-money)
        deposit = Transaction(To=account, Amount=money)
        self.session.add_all([withdraw, deposit])

        self.session.commit()

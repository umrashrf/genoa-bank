import json
import datetime

from ...db import Account
from .base import Base


class GetBalances(Base):

    def __init__(self, json_obj):
        super(GetBalances, self).__init__(json_obj) # initiates self.session

    def format(self):
        name = self.json_obj.get('account')
        accounts = self.session.query(Account).filter_by(Name=name)
        balances = {}
        for account in accounts:
            if account.Currency not in balances:
                balances[account.Currency] = sum([t.Amount for t in account.Transaction])
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return json.dumps(dict(date=today, balances=balances))


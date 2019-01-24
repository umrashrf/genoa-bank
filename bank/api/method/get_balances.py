import json
import datetime

from sqlalchemy import and_

from ... import settings
from ...db import Account, Transaction
from .base import Base

class GetBalances(Base):

    def __init__(self, json_obj):
        super(GetBalances, self).__init__(json_obj) # initiates self.session

    def toJSON(self):
        date = datetime.datetime.strptime(self.json_obj.get('date'), settings.DATE_FORMAT).date()
        name = self.json_obj.get('account')
        accounts = self.session.query(Account).filter_by(Name=name)
        balances = {}
        for account in accounts:
            transactions = self.session.query(Transaction).filter(and_(Transaction.Account == account.Id,
                                                                        Transaction.Date == date))
            if account.Currency not in balances:
                balances[account.Currency] = 0
            balances[account.Currency] += sum([t.Amount for t in transactions])
        return json.dumps(dict(date=date.strftime(settings.DATE_FORMAT), balances=balances))


import os
import json
import runpy
import logging
import unittest

from bank import settings


class TestDeposit(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

        settings.DATABASE_URI = 'sqlite:///test.db'
        runpy.run_module('bank.db',
                         {'settings.DATABASE_URI': settings.DATABASE_URI},
                         '__main__')

    def perform_action(self, json_raw, action_class):
        json_obj = json.loads(json_raw)
        action = action_class(json_obj)

        from bank.db import Currency, Account, Transaction

        ccy = json_obj.get('ccy').upper()
        currency = action.session.query(Currency).filter_by(Value=ccy).first()
        assert currency

        name = json_obj.get('account')
        account = action.session.query(Account).filter_by(Name=name,
                                                          Currency=currency.Value).first()
        assert account

        amt = json_obj.get('amt')
        money = sum([ts.Amount for ts in account.Transactions])
        assert money == amt

    def test_deposit(self):
        json_raw = '{"method": "deposit", "account": "bob", "amt" : 10, "ccy": "EUR"}'
        from bank.api.method import Deposit
        self.perform_action(json_raw, Deposit)

    def test_withdrawal(self):
        json_raw = '{"method": "withdrawal", "account": "alice", "amt" : 10, "ccy": "EUR"}'
        from bank.api.method import Withdrawal
        self.perform_action(json_raw, Withdrawal)

    def test_transfer(self):
        from bank.api.method import Deposit, Transfer

        # get some data first
        json_raw = '{"method": "deposit", "account": "alice", "amt" : 100, "ccy": "GBP"}'
        self.perform_action(json_raw, Deposit)

        # get some data first
        json_raw = '{"method": "deposit", "account": "bob", "amt" : 10, "ccy": "GBP"}'
        self.perform_action(json_raw, Deposit)

        json_raw = '{"method": "transfer", "from_account": "alice", "to_account": "bob", "amt" : 100, "ccy": "GBP"}'
        json_obj = json.loads(json_raw)
        action_class = Transfer
        action = action_class(json_obj)

        from bank.db import Currency, Account, Transaction

        ccy = json_obj.get('ccy').upper()
        currency = action.session.query(Currency).filter_by(Value=ccy).first()
        assert currency

        from_name = json_obj.get('from_account')
        from_account = action.session.query(Account).filter_by(Name=from_name,
                                                               Currency=currency.Value).first()
        assert from_account

        amt = 100 - json_obj.get('amt')
        from_money = sum([ts.Amount for ts in from_account.Transactions])
        assert from_money == amt

        to_name = json_obj.get('to_account')
        to_account = action.session.query(Account).filter_by(Name=to_name,
                                                             Currency=currency.Value).first()
        assert to_account

        amt = 10 + json_obj.get('amt')
        to_money = sum([ts.Amount for ts in to_account.Transactions])
        assert to_money == amt

    def test_get_balances(self):
        from bank.api.method import Deposit, GetBalances

        # get some data first
        json_raw = '{"method": "deposit", "account": "bob", "amt" : 10, "ccy": "EUR"}'
        self.perform_action(json_raw, Deposit)

        # get some data first
        json_raw = '{"method": "deposit", "account": "bob", "amt" : 10, "ccy": "GBP"}'
        self.perform_action(json_raw, Deposit)

        json_raw = '{"method": "get_balances", "date": "2018-10-01", "account": "bob"}'
        json_obj = json.loads(json_raw)
        action_class = GetBalances
        action = action_class(json_obj)

        json_output = action.toJSON()
        output = json.loads(json_output)
        assert 'balances' in output
        assert 'EUR' in output['balances']
        assert 'GBP' in output['balances']
        assert 'USD' not in output['balances']

    def tearDown(self):
        try:
            os.remove(os.path.basename(settings.DATABASE_URI))
        except:
            pass

if __name__ == '__main__':
    unittest.main()

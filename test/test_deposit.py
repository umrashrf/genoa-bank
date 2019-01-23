import os
import json
import runpy
import unittest

class TestDeposit(unittest.TestCase):


    def setUp(self):
        runpy.run_module('bank.db')

    # def test_basic(self):
    #     json_raw = "{'method': 'deposit', 'account': 'bob', 'amt' : 10, 'ccy': 'EUR'}"
    #     json_obj = json.loads(json_raw)
    #     from bank.api.method import Deposit
    #     action = Deposit(json_obj)

    #     from bank.db import Currency, Account

    #     ccy = json_obj.get('ccy').upper()
    #     currency = action.session.query(Currency).filter(Value=ccy).first()
    #     assert currency

    #     name = json_obj.get('account')
    #     account = action.session.query(Account).filter(Name=name,
    #                                                    Currency=currency).first()
    #     assert account

    #     amt = json_obj.get('amt')
    #     money = action.session.query(Transaction).filter(Account=account,
    #                                                      Amount=amt).first()
    #     assert money

    # def tearDown(self):
    #     os.remove(settings.DATABASE_URI.split('/')[-1])

if __name__ == '__main__':
    unittest.main()

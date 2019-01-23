from .deposit import Deposit


class Withdrawal(Deposit):

    def __init__(self, json_obj):
        # withdraw is just negative deposit
        json_obj['amt'] = 0 - json_obj['amt']
        super(Withdrawal, self).__init__(json_obj)

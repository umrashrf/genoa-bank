from .deposit import Deposit


# withdraw is just negative deposit given required balance
class Withdrawal(Deposit):

    def __init__(self, json_obj):
        # FIXME: check for required balance
        json_obj['amt'] = 0 - json_obj['amt']
        super(Withdrawal, self).__init__(json_obj)

import json

import tornado.web
import tornado.websocket

METHODS = ['deposit', 'withdrawal', 'transfer', 'get_balances']

class BankWebSocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        try:
            json_obj = json.loads(message)
        except ValueError:
            self.write_message("Invalid JSON")
            return

        method = json_obj.get('method').lower()
        if method not in METHODS:
            self.write_message('Invalid method provided (%s)' % method)
            return

        from .method import Deposit, Withdrawal, Transfer, GetBalances

        if method == 'deposit':
            Action = Deposit
        elif method == 'withdrawal':
            Action = Withdrawal
        elif method == 'transfer':
            Action = Transfer
        elif method == 'get_balances':
            Action = GetBalances

        json_output = Action(json_obj).toJSON()
        self.write_message(json_output)

    def on_close(self):
        print("WebSocket closed")

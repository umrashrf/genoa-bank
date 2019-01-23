import logging

import tornado.web

from .. import settings
from . import BankWebSocket

application = tornado.web.Application([
    (r"/websocket", BankWebSocket),
])
application.listen(settings.WEBSOCKET_PORT)
logging.info('Starting web socket on http://localhost:%s/websocket', settings.WEBSOCKET_PORT)
tornado.ioloop.IOLoop.current().start()

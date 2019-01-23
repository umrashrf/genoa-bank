import os

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///bank.db')

WEBSOCKET_PORT = 5656

DEFAULT_CURRENCY = 'EUR'

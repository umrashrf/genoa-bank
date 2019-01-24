import os
import datetime

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///bank.db')

WEBSOCKET_PORT = 5656

DEFAULT_CURRENCY = 'EUR'

# DANGER
TIMEZONE = datetime.timezone.utc

DATE_FORMAT = '%Y-%m-%d'

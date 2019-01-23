import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ... import settings
from ...db import Currency


class Base:

    def __init__(self, json_obj):
        self.json_obj = json_obj
        eng = create_engine(settings.DATABASE_URI)
        Session = sessionmaker(bind=eng)
        self.session = Session()

    def get_currency(self):
        ccy = self.json_obj.get('ccy', settings.DEFAULT_CURRENCY).upper()
        currency = self.session.query(Currency) \
                               .filter_by(Value=ccy) \
                               .first()
        if not currency:
            raise 'Invalid Currency'
        return currency

    def toJSON(self):
        return json.dumps('{}')

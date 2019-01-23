from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ... import settings

class Base:

    def __init__(self, json_obj):
        self.json_obj = json_obj
        eng = create_engine(settings.DATABASE_URI)
        Session = sessionmaker(bind=eng)
        self.session = Session()

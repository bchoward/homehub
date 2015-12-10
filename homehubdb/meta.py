from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

__all__ = ['Session', 'metadata']

engine = None
session = scoped_session(sessionmaker())
metadata = MetaData()


def init_model(eng):
    engine = eng
    session.configure(bind=eng)
    metadata.bind = eng

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from homehubdb.base import Base
from homehubdb.config import BaseConfiguration as conf

__all__ = ['Session', 'metadata']

engine = None
session = scoped_session(sessionmaker())
metadata = MetaData()


def init_model(eng):
    engine = eng
    session.configure(bind=eng)
    metadata.bind = eng
    Base.metadata.bind = engine


def setup_connection():
    engine = create_engine(conf.DB_URI)
    init_model(engine)

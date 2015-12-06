import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.base import Base
from homehub.homehub.model import *
from homehub.homehub.util import dbname


def getEventType(tbl):
    return  session.query(EventType) \
        .join(EventFamily) \
        .filter(EventType.name == tbl) \
        .filter(EventFamily.name == 'macquarium') \
        .first()


class MacquariumTemp(Base):
    __tablename__   = 'macquarium_temp'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    surface_temp    = Column(Integer, nullable=False)
    deep_temp       = Column(Integer, nullable=False)
    Event           = relationship(Event, backref='MacquariumTemp',
                                   foreign_keys='event.id')

    def __init__(self):
        self.event = Event(getEventType(self.__tablename__, 'Macqarium Temp'))
        # TODO: add code for the probes


class MacquariumDepth(Base):
    __tablename__   = 'macquarium_depth'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    depth            = Column(Integer, nullable=False)
    Event           = relationship(Event, backref='MacquariumDepth',
                                   foreign_keys='event.id')

    def __init__(self):
        self.event = Event(getEventType(self.__tablename__, 'Macqarium Depth'))

class MacquariumHeater(Base):
    __tablename__   = 'macquarium_heater'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    activated       = Column(Boolean, nullable=False)
    Event           = relationship(Event, backref='MacquariumHeater',
                                   foreign_keys='event.id')

    def __init__(self):
        self.event = Event(getEventType(self.__tablename__, 'Macqarium Heater'))

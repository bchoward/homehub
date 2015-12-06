from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.base import Base

import datetime

class EventFamily(Base):
    __tablename__ = 'event_family'
    id			    = Column(Integer, primary_key = True)
    name            = Column(Text, nullable=False)

    def __init__(self,name):
        self.name = name

class EventType(Base):
    __tablename__ = 'event_type'
    id			    = Column(Integer, primary_key = True)
    name            = Column(Text, nullable=False)
    family_id       = Column(Integer, ForeignKey('event_family.id'))
    EventFamily          = relationship(EventFamily, backref='EventType',
                                   foreign_keys='event_family.id')

    def __init__(self,name, eventfamily):
        self.name = name
        self.EventFamily = eventfamily


class Event(Base):
    __tablename__ = 'event'
    #__table_args__ =
    id			    = Column(Integer, primary_key = True)
    evtype            = Column(Integer, ForeignKey('event_type.id'))
    when		    = Column(DateTime(timezone=True))
    blurb           = Column(Text, nullable=True)
    EventType       = relationship(EventType, backref='Event',
                                   foreign_keys='event_type.id')

    def __init__(self, eventtype, blurb):
        self.when = datetime.datetime.now()
        self.blurb = blurb
        self.EventType = eventtype

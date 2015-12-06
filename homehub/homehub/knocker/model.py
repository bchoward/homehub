from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.model import *
from homehub.homehub.base import Base
from homehub.homehub.common.photo import Picture

import datetime


class DoorKnock(Base):
    __tablename__   = 'door_knock'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    picture_id      = Column(Integer, ForeignKey('picture.id'))
    Event           = relationship(Event, backref='DoorKnock',
                                   foreign_keys='event.id')
    Picture           = relationship(Picture, backref='DoorKnock',
                                   foreign_keys='picture.id')




from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.base import Base
from homehub.homehub.model.events import *
from homehub.homehub.model.users import *
#from homehub.homehub.mrfc522.rfid import (
#    DataToString,
#    StringToData,
#)

# TODO:  reimplement or fix these to work with non-python solution

import datetime

def getEventType(tbl):
    return session.query(EventType) \
        .join(EventFamily) \
        .filter(EventType.name == tbl) \
        .filter(EventFamily.name == 'door') \
        .first()



class UserRRID(Base):
    __tablename__   = 'user_rfid'
    hhuser_id         = Column(Integer, ForeignKey('hhuser.id'))
    uid             = Column(Text, nullable=False)
    key             = Column(Text, nullable=False)
    HHUser         = relationship(HHUser, backref='UserRFID',
                                   foreign_keys='hhuser.id')

    def __init__(self, user, uid, key):
        self.HHUser = user
        self.uid = uid # let's not worry about collisions...
        self.key = key

    @classmethod
    def byUid(uid):
        return session.query(HHUser).filter(HHuser.uid == DataToString(uid)).first()



class RFIDEvent(Base):
    __tablename__    = 'rfid_event'
    id			     = Column(Integer, primary_key = True)
    event_id         = Column(Integer, ForeignKey('event.id'))
    uid              = Column(Text, nullable=False)
    successful       = Column(Boolean, nullable=False)
    key              = Column(Text, nullable=True)
    Event            = relationship(Event, backref='BluetoothDetect',
                                   foreign_keys='event.id')

    def __init__(self, uid, successful, key=None):
        self.event = Event(getEventType(self.__tablename__), "RFID Authentication Event")
        self.uid = DataToString(uid)
        self.successful = successful
        self.key = key

    @classmethod
    def user_authenticated(user, uid, key):
        re = RFIDEvent(uid, True, key)
        session.add(re)
        reu = RFIDEventHHUser(re.Event, user)
        session.add(reu)
        session.commit()


    @classmethod
    def authentication_error(uid):
        re = RFIDEvent(uid, False, key = None)
        session.add(re)
        session.commit()


class RFIDEventHHUser(Base):
    __tablename__    = 'rfid_event_hhuser'
    rfid_event_id    = Column(Integer, ForeignKey('rfid_event.id'))
    hhuser_id        = Column(Integer, ForeignKey('hhuser.id'))
    RFIDEvent            = relationship(RFIDEvent, backref='RFIDEventHHUser',
                                   foreign_keys='rfid_event.id')
    HHUser           = relationship(HHUser, backref='RFIDEventHHUser',
                                   foreign_keys='hhuser.id')

    def __init__(self, event, hhuser):
        self.event = event
        self.hhuser = hhuser



#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehubdb.meta import session
from homehubdb.base import Base
from homehubdb.model.events import *
from homehubdb.model.users import *

import datetime
#from bluetooth import DeviceDiscoverer
from io.bluetooth.bt import DeviceDiscoverer
from io.bluetooth.bt import BluetoothDeviceDetector
import select
import os
import re

DEBUG = True
WRITE_DB = True


def getEventType(tbl):
    return session.query(EventType) \
        .join(EventFamily) \
        .filter(EventType.name == tbl) \
        .filter(EventFamily.name == 'door') \
        .first()



class HHUserBTAddr(Base):
    __tablename__ = 'hhuser_btaddr'
    hhuser        = Column(Integer, ForeignKey('hhuser.id'), primary_key=True)
    btaddr        = Column(Text, nullable=False, primary_key=True)
    HHUser           = relationship(HHUser, backref='BTAddresses',
                                   foreign_keys='hhuser.id')



class BluetoothDetect(Base):
    __tablename__ = 'bluetooth_detect'
    id		    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    device_id       = Column(Text, nullable=False)
    device_name     = Column(Text, nullable=False)
    activated       = Column(Boolean, nullable=False)
    device_info     = Column(Text, nullable=True)
    Event           = relationship(Event, backref='BluetoothDetect',
                                   foreign_keys='event.id')

    def __init__(self, msg, device_id, activated, name, device_info=None):
        self.event = Event(getEventType(self.__tablename__), "Bluetooth device detected")
        self.device_id = device_id
        self.activated = activated
        self.device_info = device_info
        self.device_name = name





class BluetoothDeviceDetect(Base):
    __tablename__ = 'bluetooth_device_detect'
    id		    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    device_id       = Column(Text, nullable=False)
    device_name     = Column(Text, nullable=False)
    Event           = relationship(Event, backref='BluetoothDeviceDetect',
                                   foreign_keys='event.id')

    def __init__(self, msg, device_id, name):
        self.event = Event(getEventType(self.__tablename__), "Bluetooth device detected")
        self.device_id = device_id
        self.device_name = name



    @staticmethod
    def detect_users():
        user_addrs = session.query(HHUserBTAddr)
        addr_list = [u.btaddr for u in user_addrs]
        ddict = BluetoothDeviceDetector.detect_dict(addr_list)
        if ddict:
            for ua in user_addrs:
                if ua.btaddr in ddcit.keys:
                    x = BluetoothDeviceDetector('BluetoothDeviceDetect',
                                              ua.btaddr, ddict[ua.btaddr]
                                              )
                    session.add(x)
                    session.commit()









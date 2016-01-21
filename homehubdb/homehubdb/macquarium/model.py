import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehubdb.meta import session
from homehubdb.base import Base
from homehubdb.model import *
from sensors import *

"""
from pypinsobj import *
p.add(23, 'temp_sensor', IN) 
p.add(24, 'doorbell', IN) 
p.add(22, 'test_LED', OUT)
p.add(25, 'latch', OUT)
p.add(1, 'vcc', RESERVED, 'connected to positive 3v')
p.add(9, 'MISO', RESERVED, 'used for MISO SPI')

...

if p.input('temp_sensor'):
           p.turn_on('test_LED')


def doorbell_cb(pin):
        if pin == p.getp('doorbell'):
                    p.turn_on('latch')
        sleep(2)
        p.turn_off('latch')

wait_event('doorbell', RISING, callback=doorbell_cb, bouncetime=200)

GPIO.cleanup()
"""

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
    ambient_temp    = Column(Integer, nullable=False)
    Event           = relationship(Event, backref='MacquariumTemp',
                                   foreign_keys='event.id')

    def __init__(self):
        self.event = Event(getEventType(self.__tablename__, 'Macqarium Temp'))
        self.surface_temp, self.deep_temp self.ambient_temp= get_temps()




class MacquariumDepth(Base):
    __tablename__   = 'macquarium_depth'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    depth            = Column(Integer, nullable=False)
    Event           = relationship(Event, backref='MacquariumDepth',
                                   foreign_keys='event.id')

    def __init__(self):
        self.event = Event(getEventType(self.__tablename__, 'Macqarium Depth'))
        self.depth = get_depth()



"""
class MacquariumHeater(Base):
    __tablename__   = 'macquarium_heater'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    activated       = Column(Boolean, nullable=False)
    Event           = relationship(Event, backref='MacquariumHeater',
                                   foreign_keys='event.id')

    def __init__(self):
        self.event = Event(getEventType(self.__tablename__, 'Macqarium Heater'))
"""

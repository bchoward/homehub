from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.model import *
from homehub.homehub.base import Base

import datetime

from bluetooth import DeviceDiscoverer
import select

DEBUG = True
WRITE_DB = True


def getEventType(tbl):
    return session.query(EventType) \
        .join(EventFamily) \
        .filter(EventType.name == tbl) \
        .filter(EventFamily.name == 'door') \
        .first()




class BluetoothDetect(Base):
    __tablename__ = 'bluetooth_detect'
    id			    = Column(Integer, primary_key = True)
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


class MyDiscoverer(DeviceDiscoverer):

## adapted from:
## https://github.com/karulis/pybluez/blob/master/examples/simple/asynchronous-inquiry.py
# file: asynchronous-inquiry.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: demonstration of how to do asynchronous device discovery by subclassing
#       the DeviceDiscoverer class
# $Id: asynchronous-inquiry.py 405 2006-05-06 00:39:50Z albert $
#


    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, address, device_class, rssi, name):

        device_info = {}
        device_info['address'] = address
        device_info['name'] = name
        device_info['rssi'] = str(rssi)
        # get some information out of the device class and display it.
        # voodoo magic specified at:
        #
        # https://www.bluetooth.org/foundry/assignnumb/document/baseband
        major_classes = ( "Miscellaneous",
                          "Computer",
                          "Phone",
                          "LAN/Network Access point",
                          "Audio/Video",
                          "Peripheral",
                          "Imaging" )
        major_class = (device_class >> 8) & 0xf
        if major_class < 7:
            device_info['major_class'] = major_classes[major_class]
        else:
            device_info['major_class'] = "Uncategorized"

        service_classes = ( (16, "positioning"),
                            (17, "networking"),
                            (18, "rendering"),
                            (19, "capturing"),
                            (20, "object transfer"),
                            (21, "audio"),
                            (22, "telephony"),
                            (23, "information"))

        device_info['services'] = []
        for bitpos, classname in service_classes:
            if device_class & (1 << (bitpos-1)):
                device_info['services'].append(classname)

        if DEBUG:
            print device_info

        if WRITE_DB:
            event = Event()
            bt = BluetoothDetect(event, address, True, name, str(device_info))

        def inquiry_complete(self):
            self.done = True

def main():
    d = MyDiscoverer()
    d.find_devices(lookup_names = True)
    readfiles = [ d, ]

    while True:
        rfds = select.select( readfiles, [], [] )[0]
        if d in rfds:
            d.process_event()
        if d.done: break


if __name__ == "__main__":
    main()

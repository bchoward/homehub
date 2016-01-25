#!/usr/bin/env python

import datetime
import subprocess
from subprocess import CalledProcessError
from bluetooth import DeviceDiscoverer
import select
import os
import re

from sqlalchemy import *

from homehubdb.base import *
from homehubdb.meta import *
from homehubdb.model.events import *
from homehubdb.model.bt import *
from homehubdb.model.users import *

DEBUG = True
WRITE_DB = True




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

class BluetoothDeviceDetector(object):
                                   foreign_keys='event.id')



    @staticmethod
    def detect(btaddress):
        try:
            cmd = ['/usr/bin/hcitool', 'info', btaddress]
            devnull = open(os.devnull, 'w')
            kwargs = {'stderr':devnull}
            #kwargs = {'stderr':subprocess.STDOUT}
            output = subprocess.check_output(cmd) #, **kwargs)
            #print "output = {}".format(output)
            m = re.search(r'^\s+Device Name:\s+(.*)', str(output), re.MULTILINE)
            if m:
                return m.group(1)
        except CalledProcessError as e:
            #print e
            return None
        return None

    @staticmethod
    def detect_list(addr_list):
        return [BluetoothDeviceDetector.detect(a) for a in addr_list]

    @staticmethod
    def detect_dict(addr_list):
        return {key: BluetoothDeviceDetector.detect(key) for key in addr_list}

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









#!/usr/bin/env python

from homehubdb.common.bt import *

import datetime


sleep_int = 10
btaddrs = [ '18:F6:43:4E:DB:6B', # bch
            ]


def main():
    while True:
        rs = BluetoothDeviceDetect.detect_dict(btaddrs)
        for (k,v) in rs:
            print "address {} is {} ({})".format(k, \
                                                 'Present' if rs[k] else 'Absent',
                                                 rs[k])
        sleep(sleep_int)




if __name__ == "__main__":
    main()

#!/usr/bin/env python

from homehubdb.common.bt import *

import datetime


sleep_int = 10
btaddrs = [ '18:F6:43:4E:DB:6B', # bch
            ]


def main():
    d = {key:None for key in btaddrs}
    while True:
        rs = BluetoothDeviceDetect.detect_dict(btaddrs)
        """
        for (k,v) in rs:
            print "address {} is {} ({})".format(k, \
                                                 'Present' if rs[k] else 'Absent',
                                                 rs[k])
        """
        print d
        for k in d.keys:
            if d[k] != rs[k]:
                d[k] = rs[k]
                if rs[k]:
                    print "address {} in range".format(k)
                else:
                    print "address {} left ".format(k)
        sleep(sleep_int)




if __name__ == "__main__":
    main()

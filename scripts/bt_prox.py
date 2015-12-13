#!/usr/bin/env python

from homehubdb.common.bt import *

import datetime
import time


sleep_int = 3
btaddrs = [ '18:F6:43:4E:DB:6B', # bch
            ]


def main():
    d = {key:None for key in btaddrs}
    while True:
        rs = BluetoothDeviceDetect.detect_dict(btaddrs)
        for k in d.keys():
            if d[k] != rs[k]:
                if rs[k]:
                    print "address {} ({}) in range".format(k, rs[k])
                else:
                    print "address {} ({}) left ".format(k, rs[k])
                d[k] = rs[k]
        time.sleep(sleep_int)




if __name__ == "__main__":
    main()

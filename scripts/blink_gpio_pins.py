#!/usr/bin/env python

import os, datetime, re, sys
from time import sleep

from pypinsobj.pypinsobj import *


def main():
    p = Pins(mode=BCM)
    #testpins = [12,21]
    args = sys.argv[1:]
    if args:
	testpins = args
    else:
	print "e.g. blink_gpio_pins.py 12 21"
    for x in testpins:
        p.add(x, 'test'+str(x), OUT)

    # 
    sleep_time = 1
    while True:
        sleep(sleep_time)
        for x in testpins:
            p.turn_on('test'+str(x))
        print "on"
        sleep(sleep_time)
        for x in testpins:
            p.turn_off('test'+str(x))
        print "off"




if __name__ == '__main__':
    main()




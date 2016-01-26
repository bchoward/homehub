#!/usr/bin/env python

import os, datetime, re

#from io.distance.hcsr04 import sensor
from hcsr04sensor import sensor
from pypinsobj.pypinsobj import *


TEST_PIN = -1



def callback():
    if p.input('test'):
	print "high"
    else:
	print "low"



def main():
    p = Pins(mode=BCM)

    arg = 
    if len(sys.argv) >= 2::
	TEST_PIN = sys.argv[1]
    else:
	print "e.g. listen_pin.py 12 "
	sys.exit()


    p.add(TEST_PIN, 'test', IN)
    print "startup"
    callback()
    print "###"
    p.wait_event('test',BOTH, callback=callback)


    while True:
	pass




if __name__ == '__main__':
    main()




#!/usr/bin/env python

from io.bluetooth.bt import *

import datetime

import select

DEBUG = True
WRITE_DB = True


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

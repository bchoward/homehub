#!/usr/bin/env python

from homehub.meta import session
from homehub.homehub.model import *
from homehub.homehub.common.bt import *
from homehub.homehub.base import Base

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

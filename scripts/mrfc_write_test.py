#!/usr/bin/env python
# -*- coding: utf8 -*-

from sqlalchemy import *

from homehubdb.mfrc522 import mfrc522 as MIFAREReader

import RPi.GPIO as GPIO
import signal
import random
import argparse
import sys


def main():
    MIFAREReader = MFRC522()

    # Welcome message
    print "Welcome to the MFRC522 data write example"

    def auth_callback(uid):
        print "detected uid {}".format(uid)
        return None

    def write_callback(uid):
        key = MIFAREReader.get_random_key()
        print "coding uid {} to key {}".format(uid, key)
        return

    MIFAREReader.read_write_card(timeout=60, auth_callback=auth_callback, \
                                 write_callback=write_callback)

    GPIO.cleanup()

if __name__ == "__main__":
    main()

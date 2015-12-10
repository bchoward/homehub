#!/usr/bin/env python
# -*- coding: utf8 -*-

from sqlalchemy import *

from homehubdb.mfrc522 import mfrc522 as MIFAREReader

import RPi.GPIO as GPIO
import signal
import random
import argparse
import sys


"""
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
"""


def main():

    # Welcome message
    print "Welcome to the MFRC522 data read example"

    def auth_callback(uid):
        print uid
        return None

    MIFAREReader.read_write_card(timeout=60, auth_callback=auth_callback)

    GPIO.cleanup()

if __name__ == "__main__":
    main()

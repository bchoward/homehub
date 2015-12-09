#!/usr/bin/env python
# -*- coding: utf8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.base import Base
from homehub.homehub.model import *
from homehub.homehub.users import *
import homehub.homehub.MFRC522
from homehub.homehub.MFRC522 import (
    DataToString,
    StringToData,
)

import RPi.GPIO as GPIO
import signal
import random
import argparse
import sys

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()


def authenticated(user, uid, key):
    re = RFIDEvent(uid, True, key)
    session.add(re)
    reu = RFIDEventHHUser(re.Event, user)
    session.add(reu)
    session.commit()




def authentication_error(uid):
    re = RFIDEvent(uid, False, key = None)
    session.add(re)
    session.commit()

def main():

    # Welcome message
    print "Welcome to the MFRC522 data read example"
    print "Press Ctrl-C to stop."

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:

        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: "+DataToString(uid)

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # see if we know this uid
            user = session.query(HHUser).filter(HHUser.uid == DataToString(uid)).first()
            if not user:
                continue
            key = user.key

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                authenticated(user, uid, data)
            else:
                print "Authentication error"
                authentication_error(uid)

if __name__ == "__main__":
    main()

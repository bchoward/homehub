#!/usr/bin/env python

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

### TODO:  check out http://bsd.ee/~hadara/blog/?p=1017 for guidance on what
### to install and add that to the README

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


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument('-u', '--user', help='username to associate card with'
                    , required = True)
    username = args.user
    user = session.query(HHUser).filter(HHUser.name == username).first()
    if not user:
        print "Could not find user {} in the database!".format(username)
        sys.exit()


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
            print "Card read UID: "+ MIFAREReader.DataToString(uid)

            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            print "\n"

            # Check if authenticated
            if status == MIFAREReader.MI_OK:

                # Variable for the data to write
                data = []

                # Fill the data with 0xFF
                for i in range(0,16):
                    x = random.randint(0,255)
                    data.append(x)

                print "Sector 8 looked like this:"
                # Read block 8
                MIFAREReader.MFRC522_Read(8)
                print "\n"

                print "Sector 8 will now be filled with new uid:"
                print "..."
                # Write the data
                MIFAREReader.MFRC522_Write(8, data)

                print "It now looks like this:"
                # Check to see if it was written
                new_key = MIFAREReader.MFRC522_Read(8)
                print "\n"

                # Stop
                MIFAREReader.MFRC522_StopCrypto1()

                # Make sure to stop reading for cards
                continue_reading = False

                if DataToString(new_key) == DataToString(data):
                    # success
                    u = UserRFID(user,DatToString(uid),DataToString(data))
                    session.add(u)
                    session.commit()
            else:
                print "Authentication error"


if __name__ == '__main__':
    main()

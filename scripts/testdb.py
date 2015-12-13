#!/usr/bin/env python

from sqlalchemy import *

import os, datetime, re

from homehubdb.meta import session
from homehubdb.meta import setup_connection
from homehubdb.model import *
from homehubdb.common.bt import BluetoothDetect
from homehubdb.common.photo import Picture
#from homehubdb.knocker.model import *
#from homehubdb.macquarium.model import *


os.environ['PYTHONINSPECT'] = 'True'

setup_connection()

def main():
    pass


if __name__ == '__main__':
    main()



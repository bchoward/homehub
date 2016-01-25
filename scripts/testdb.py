#!/usr/bin/env python

from sqlalchemy import *

import os, datetime, re

from homehubdb.meta import session
from homehubdb.meta import setup_connection
from homehubdb.model.events import *


os.environ['PYTHONINSPECT'] = 'True'

setup_connection()

def main():
    pass


if __name__ == '__main__':
    main()



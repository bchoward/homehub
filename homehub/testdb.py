import homehub

import os, datetime, re
from sqlalchemy import *
from wsgi import setup_connection

from model import *
from common.bluetooth import BluetoothDetect
from common.photo import Picture
from knocker.model import *
from macquarium.model import *


os.environ['PYTHONINSPECT'] = 'True'

setup_connection()

def main():
    pass


if __name__ == '__main__':
    pass



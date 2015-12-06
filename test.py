#!/usr/bin/env python

from homehub.wsgi import setup_connection
setup_connection()
from homehub.homehub.base import Base
print Base.metadata
from homehub.homehub.model import *
from  homehub.homehub.macquarium.model import *
from  homehub.homehub.knocker.model import *
from  homehub.homehub.common.photo import *
import bluetooth
from  homehub.homehub.common.bt import BluetoothDetect

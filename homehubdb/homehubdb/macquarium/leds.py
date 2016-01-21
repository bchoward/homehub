import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehubdb.meta import session
from homehubdb.base import Base
from homehubdb.model import *

from pypinsobj import Pins


class MacquariumLEDs(Object):
    

    def __init__(self):
        self.front = False
        self.back = False

        self.p = Pins()
        self.p.add(



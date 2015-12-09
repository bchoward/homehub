from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.base import Base
from homehub.homehub.model import *

from werkzeug import generate_password_hash, check_password_hash



class HHUser(Base):
    __tablename__   = 'hhuser'
    id			    = Column(Integer, primary_key=True)
    name            = Column(Text, nullable=False, unique=True)
    role            = Column(Enum('admin', 'normal', 'guest', name='user_types'), nullable=False)
    enabled         = Column(Boolean, nullable=False)
    password        = Column(Text, nullable=False)

    def __init__(self, name, role, status):
        pass

    def __repr__(self):
        return '<User name=%r id=%d>' % (self.name,self.id)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # syntax is (hash, password)
        return check_password_hash(self.password, password)



from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.model import *
from homehub.homehub.util import dbname


import datetime
import argparse
import tempfile

#import picamera

FORMAT='jpeg'



class Camera():

    def __init__():
        self.camera = picamera.PiCamera()
        self.format = FORMAT


    def capture(f):
        return camera.capture(f, format=self.format)


class Picture(Base):
    __tablename__   = 'picture'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    picture_blob    = Column(BLOB, nullable=True)
    Event           = relationship(Event, backref='Picture',
                                   foreign_keys='event.id')

    def __init__(self, event):
        self.event = event
        c = Camera()
        tmpf = tempfile.TemporaryFile(mode='wb')
        c.capture(tmpf)
        tmpf.seek(0)
        self.picture = tmpf.read()

    @property
    def picture(self):
        return self.picture_blob


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filename', help='file to write to'
                    , required = False , action='store_true')

    # Connect to databases and crawler on GCE instance
    args = ap.parse_args()
    filename = "test." + FORMAT
    if args.filename:
        filename = args.filename

    c = Camera()
    c.capture(filename)



if __name__ == "__main__":
    __main__()


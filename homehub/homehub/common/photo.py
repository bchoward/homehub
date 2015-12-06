from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from psycopg2 import OperationalError

from homehub.meta import session
from homehub.homehub.model import *
from homehub.homehub.util import dbname
#!/usr/bin/env python
from homehub.homehub.base import Base

import datetime
import argparse
import tempfile
import platform
import re
from contextlib import contextmanager

# only import on the pi to prevent alembic from shitting itself
if re.search(r'^armv',platform.machine()):
    import picamera



FORMAT='jpeg'


class Camera():

    def __init__():
        self.camera = picamera.PiCamera()
        self.format = FORMAT


    """ supply an open-for-write file as f """
    def capture(f):
        return camera.capture(f, format=self.format)


class Picture(Base):
    __tablename__   = 'picture'
    id			    = Column(Integer, primary_key = True)
    event_id        = Column(Integer, ForeignKey('event.id'))
    loid            = Column(Integer, nullable=False)
    Event           = relationship(Event, backref='Picture',
                                   foreign_keys='event.id')

    def __init__(self, event):
        self.event = event
        self.loid = 0
        c = Camera()
        with self.get_lobject(mode='wb') as fd:
            c.capture(fd)




    """ returns a file that can be read() from """
    @property
    def picture_fd(self):
        return self.get_lobject()

    """ returns data from from the lob """
    @property
    def picture(self):
        return self.picture_fd().read()


    @contextmanager
    def get_lobject(self, mode=None):
        """Return an open file bounded to the represented large
        object. This is a context manager, so it should be used with
        the `with' clause this way:

          with fsobject.get_lobject() as lo:

        mode (string): how to open the file (r -> read, w -> write,
                       b -> binary). If None, use `rb'.

        """
        if mode is None:
            mode = 'rb'

        # Here we rely on the fact that we're using psycopg2 as
        # PostgreSQL backend
        lo = session.connection().connection.lobject(self.loid, mode)

        if self.loid == 0:
            self.loid = lo.oid

        try:
            yield lo
        finally:
            lo.close()

    def check_lobject(self):
        """Check that the referenced large object is actually
        available in the database.

        """
        try:
            lo = session.connection().connection.lobject(self.loid)
            lo.close()
            return True
        except OperationalError:
            return False

    def delete(self):
        """Delete this file.

        """
        with self.get_lobject() as lo:
            lo.unlink()
        session.delete(self)

    @classmethod
    def get_all(cls, session):
        """Iterate over all the FSObjects available in the database.

        """
        if cls.__table__.exists():
            return session.query(cls)
        else:
            return []

    @classmethod
    def delete_all(cls, session):
        """Delete all files stored in the database. This cannot be
        undone. Large objects not linked by some FSObject cannot be
        detected at the moment, so they don't get deleted.

        """
        for fso in cls.get_all(session):
            fso.delete()

    def export_to_dict(self):
        """FSObjects cannot be exported to a dictionary.

        """
        return {}





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


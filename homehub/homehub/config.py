import os
from ConfigParser import ConfigParser


_basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfiguration(object):
    conf = ConfigParser()
    conf.read('homehub/config.ini')
    DB_URI= conf.get('homehub', 'DB_URI')

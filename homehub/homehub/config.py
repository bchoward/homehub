from os.path import (
    join as ospjoin,
    dirname,
    abspath
)
from ConfigParser import ConfigParser


_basedir = abspath(dirname(__file__))


class BaseConfiguration(object):
    conf = ConfigParser()
    #conf.read('homehub/config.ini')
    conf.read(ospjoin(_basedir,'homehub','config.ini'))
    DB_URI= conf.get('homehub', 'DB_URI')

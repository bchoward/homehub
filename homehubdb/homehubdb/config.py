from ConfigParser import ConfigParser
from os.path import (
    join as ospjoin,
    dirname,
    abspath
)


_basedir = abspath(dirname(__file__))


class BaseConfiguration(object):
    conf = ConfigParser()
    #conf.read('homehub/config.ini')
    config_path =ospjoin(_basedir,'..','config.ini')
    print config_path
    conf.read(config_path)
    DB_URI= conf.get('homehub', 'DB_URI')

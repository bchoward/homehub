#Python/sqlalchemy system for home automation (door monitoring, fishtank, etc)


##Required for installation:
apt-get install bluez
apt-get install libbluetooth-dev


##Omitted from github:
- /alembic.ini (stock except for sqlalchemy.url)
- /homehub/config.ini (use this):
        [homehub]
        DB_URI=postgresql://username:password@host:port/dbname


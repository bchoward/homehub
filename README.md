#Python/sqlalchemy system for home automation (door monitoring, fishtank, etc)


##Required for installation:
```
apt-get install bluez libbluetooth-dev python-bluez python-picamera python-sqlalchemy python-pip libpython-dev python-psycopg2 postgresql-doc postgresql-client postgresql-client-common libpq-dev 
```

## installation
```
git clone [copied]

cd homehub
pip install --user vex
echo "PATH=$PATH:$HOME/.local/bin" >> ~./.bashrc
vex -m homehub
```
Add to ~/.bashrc:
```
echo "alias vhh='vex homehub'" >> ~./.bashrc
# vex prompt
function virtualenv_prompt() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "(${VIRTUAL_ENV##*/}) "
    fi  
}
export PS1='$(virtualenv_prompt)\u@\H:\w\$ '
```
then, logout and back in:
```
cd homehub
vhh
pip install -r requirements.txt


```


##Omitted from github:
- /alembic.ini (stock except for sqlalchemy.url)
- /homehub/config.ini (use this):
```
[homehub]
    DB_URI=postgresql://username:password@host:port/dbname
```

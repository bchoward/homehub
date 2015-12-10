#Python/sqlalchemy system for home automation (door monitoring, fishtank, etc)


##Required for installation:
```
sudo apt-get install bluez libbluetooth-dev python-bluez python-picamera python-sqlalchemy python-pip libpython-dev python-psycopg2 postgresql-doc postgresql-client postgresql-client-common libpq-dev python-dev
```

## installation

clone using HTTPS, and you have to do pw authentication
clone using SSH (from pulldown menu on repo page) and you can use ssh keys

```
git clone [copied]

cd homehub
pip install --user vex
echo "PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc
vex -m homehub
```
Add to ~/.bashrc:
```
echo "alias vhh='vex homehub'" >> ~/.bashrc
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
git clone git@github.com:bchoward/pypinsobj.git
git clone https://github.com/alaudet/hcsr04sensor.git
git clone https://github.com/doceme/py-spidev.git
git clone https://github.com/lthiery/SPI-Py
git clone https://github.com/bchoward/MFRC522-python.git
mv MRFC522-python mrfc522
cd py-spidev
python setup.py install
cd ..
pip install -r requirements.local


```

for making SPI work (needed for mrfc522) as per
[here](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md)
```
The SPI master driver is disabled by default on Raspian. To enable it, remove
the blacklisting for spi-bcm2708 in /etc/modprobe.d/raspi-blacklist.conf,
or use raspi-config. Reboot or load the driver manually with:

$ sudo modprobe spi-bcm2708
```


##Omitted from github:
- /alembic.ini (stock except for sqlalchemy.url)
- /homehub/config.ini (use this):
```
[homehub]
    DB_URI=postgresql://username:password@host:port/dbname
```

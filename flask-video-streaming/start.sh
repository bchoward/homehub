#!/bin/bash
# run this as the rhodecode user!
HDIR=/home/pi
PROJRT=homehub
VIRTUALENV_DIR=$HDIR/.virtualenvs/$PROJRT


source $VIRTUALENV_DIR/bin/activate
cd $HDIR/$PROJRT/flask-video-streaming

$VIRTUAL_ENV/bin/python app.py

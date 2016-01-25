#!/bin/bash


HDIR=/home/pi
PROJRT=homehub/frontends
PROJNAME=flask-video-streaming
EXECNAME=app.py
VIRTUALENV_DIR=$HDIR/.virtualenvs/homehub


source $VIRTUALENV_DIR/bin/activate
cd $HDIR/$PROJRT/$PROJNAME

$VIRTUAL_ENV/bin/python $EXECNAME

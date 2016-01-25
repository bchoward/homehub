#!/bin/bash


HDIR=/home/pi
PROJRT=homehub/frontends/
PROJNAME=flask-video-streaming
EXECNAME=app.py
VIRTUALENV_DIR=$HDIR/.virtualenvs/$PROJRT


source $VIRTUALENV_DIR/bin/activate
cd $HDIR/$PROJRT/$PROJNAME-video-streaming

$VIRTUAL_ENV/bin/python $EXECNAME

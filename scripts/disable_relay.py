#!/usr/bin/env python

from RPi import GPIO
from RPi.GPIO import *
import time

GPIO.setmode(BCM)
pin = 21
GPIO.setup(pin, OUT)
output(pin, HIGH)
GPIO.cleanup()

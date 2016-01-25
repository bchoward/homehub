#!/usr/bin/env python

from io.temperature.temp_sensors import *
from io.distance.hcsr04 import *

print "available sensors:"
print list_w1_sensors()
print "----"
print "TMP 006"
#print get_TMP006_temp()
print "DS18B20"
print getDS18b20_temp()

print get_distance()

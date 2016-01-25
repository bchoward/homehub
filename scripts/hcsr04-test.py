#!/usr/bin/env python

import os, datetime, re

#from io.distance.hcsr04 import sensor
from hcsr04sensor import sensor
from pypinsobj.pypinsobj import *


def main():
    '''Example script using hcsr04sensor module for Raspberry Pi'''
    p = Pins(mode=BCM)
    p.add(20, 'echo', IN)
    p.add(21, 'trig', OUT)
    unit = 'metric'  # choices (metric or imperial)
    temperature = 16  # Celcius for metric, Fahrenheit for imperial
    round_to = 1  # report a cleaner rounded output.

    #  Create a distance reading with the hcsr04 sensor module
    value = sensor.Measurement(p.getp('trig'), p.getp('echo'), temperature, unit, round_to)
    raw_measurement = value.raw_distance()

    # Calculate the distance in centimeters
    metric_distance = value.distance_metric(raw_measurement)
    print("distance = {} centimeters".format(metric_distance))


if __name__ == '__main__':
    main()




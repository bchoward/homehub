import datetime


DEPTH_OFFSET=0

def get_distance():
    import io.hcsr04sensor.sensor as sensor
    trig_pin = XX
    echo_pin = XX
    unit = 'metric'  # choices (metric or imperial)
    temperature = 18  # Celcius for metric, Fahrenheit for imperial
    round_to = 1  # report a cleaner rounded output.
    value = sensor.Measurement(trig_pin, echo_pin, temperature, unit, round_to)
    raw_measurement = value.raw_distance()
    metric_distance = value.distance_metric(raw_measurement)
    return metric_distance



def get_depth():
    return get_distance -DEPTH_OFFSET



"""
from pypinsobj import *
p.add(23, 'temp_sensor', IN) 
p.add(24, 'doorbell', IN) 
p.add(22, 'test_LED', OUT)
p.add(25, 'latch', OUT)
p.add(1, 'vcc', RESERVED, 'connected to positive 3v')
p.add(9, 'MISO', RESERVED, 'used for MISO SPI')

...

if p.input('temp_sensor'):
           p.turn_on('test_LED')


def doorbell_cb(pin):
        if pin == p.getp('doorbell'):
                    p.turn_on('latch')
        sleep(2)
        p.turn_off('latch')

wait_event('doorbell', RISING, callback=doorbell_cb, bouncetime=200)

GPIO.cleanup()
"""


import datetime
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
def get_temps():
    obj_temp = get_TMP006_temp()
    drok_temp = getDS18b20_temp()
    #print 'Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp, c_to_f(obj_temp))
    #print '   Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die_temp, c_to_f(die_temp))
    return obj_temp, drok_temp

def getDS18b20_temp():
    from w1thermsensor import W1ThermSensor
    #sensor = W1ThermSensor()
    #sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "a00000000000")
    sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)
    #temperature_in_celsius = sensor.get_temperature()
    return sensor.get_temperature(W1ThermSensor.DEGREES_F)


def list_w1_sensors():
    from w1thermsensor import W1ThermSensor
    for sensor in W1ThermSensor.get_available_sensors():
	print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))

def get_TMP006_temp():
    def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0
    # TMP006
    import Adafruit_TMP.TMP006 as TMP006
    sensor = TMP006.TMP006()
    sensor.begin()
    obj_temp = c_to_f(sensor.readObjTempC())
    #die_temp = c_to_f(sensor.readDieTempC())
    return obj_temp



def get_depth():
    import hcsr04sensor.sensor as sensor
    trig_pin = XX
    echo_pin = XX
    unit = 'metric'  # choices (metric or imperial)
    temperature = 18  # Celcius for metric, Fahrenheit for imperial
    round_to = 1  # report a cleaner rounded output.
    value = sensor.Measurement(trig_pin, echo_pin, temperature, unit, round_to)
    raw_measurement = value.raw_distance()
    metric_distance = value.distance_metric(raw_measurement)
    return metric_distance


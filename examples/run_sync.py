from mh_z19b.sync import Sensor

sensor = Sensor(port='/dev/cu.usbserial', baudrate=9600)
print(sensor.read_metric())
import serial

from mh_z19b.common import SensorMixin


class Sensor(SensorMixin):
    def __init__(self, **kwargs):
        super(Sensor, self).__init__(serial.Serial(**kwargs))

    def send_request(self, payload, *args):
        data = self._prepare_request(payload, *args)
        return self.serial.write(data)

    def send_receive(self, command, *args):
        self.serial.read(self.serial.in_waiting)  # flush all data in input buffer
        self.send_request(command, *args)
        return self.parse_response(self.serial.read(9))

    def read_metric(self):
        return self.send_receive(self.READ_METRIC)

    def set_detection_range(self, detection_range):
        assert detection_range in [2000, 5000], "Only 2000 and 5000 ranges are supported"
        return self.send_receive(self.SET_DETECTION_RANGE % (detection_range >> 8 & 0xff, detection_range & 0xff))

    def set_auto_calibration(self, on):
        on_off_byte = 0xA0 if on else 0x00
        return self.send_receive(self.SET_AUTO_CALIBRARTION % on_off_byte)

    def start_calibration(self):
        return self.send_receive(self.START_CALIBRATION)

import asyncio
import serial_asyncio
import binascii

from mh_z19b.common import SensorMixin


class Sensor(SensorMixin):
    def __init__(self, ioloop = None):
        if ioloop is not None:
            self.loop = ioloop
        else:
            self.loop = asyncio.get_event_loop()

    async def open_serial(self, **kwargs):
        (self.reader, self.writer) = await serial_asyncio.open_serial_connection(loop=self.loop, **kwargs)

    async def send_request(self, payload, *args):
        data = self._prepare_request(payload, *args)
        self.writer.write(data)
        await self.writer.drain()

    async def send_receive(self, command, *args):
        while True:
            await self.send_request(command, *args)
            buf = await asyncio.wait_for(self.reader.readexactly(9), timeout=3)

            result = self.parse_response(buf)
            if result is not None:
                return result
            else:
                await asyncio.sleep(1)

    async def read_metric(self):
        return await self.send_receive(self.READ_METRIC)

    async def set_detection_range(self, detection_range):
        assert detection_range in [2000, 5000], "Only 2000 and 5000 ranges are supported"
        return await self.send_receive(self.SET_DETECTION_RANGE % (detection_range >> 8 & 0xff, detection_range & 0xff))

    async def set_auto_calibration(self, on):
        on_off_byte = 0xA0 if on else 0x00
        return await self.send_receive(self.SET_AUTO_CALIBRARTION % on_off_byte)

    async def start_calibration(self):
        return await self.send_receive(self.START_CALIBRATION)

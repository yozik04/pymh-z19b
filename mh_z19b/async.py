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

    async def read_metric(self):
        return await self.send_receive(self.READ_METRIC)

    async def send_receive(self, command, *args):
        await self.send_request(command, *args)
        while True:
            buf = bytearray()
            while True:
                c = await self.reader.read(1)
                buf.append(ord(c))

                if len(buf) == 9:
                    break

            result = self.parse_response(buf)
            if result is not None:
                return result

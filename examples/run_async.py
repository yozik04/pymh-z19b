import asyncio

from mh_z19b.async import Sensor

async def run(loop):
    sensor = Sensor(loop)
    await sensor.open_serial(url='/dev/cu.usbserial', baudrate=9600)
    data = await sensor.read_metric()
    print(data)

loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(run(loop))
loop.close()
import asyncio
from sessypy.api import SessyApi
from sessypy.const import SessyApiCommand
from config import * # Hide your secrets here
from sessypy.devices import SessyP1Meter, SessyBattery

async def run():
    print("P1 Status")
    p1 = SessyP1Meter(SESSY_P1_HOST, SESSY_P1_USERNAME, SESSY_P1_PASSWORD)
    result = await p1.get_p1_status()
    print(result)
    await p1.close()
    print("")

    print("Power Status")
    battery = SessyBattery(SESSY_BATTERY_HOST, SESSY_BATTERY_USERNAME, SESSY_BATTERY_PASSWORD)
    result = await battery.get_power_status()
    print(result)
    print("")

    print("Power Strategy")
    result = await battery.get_power_strategy()
    print(result)
    print("")
    
    await battery.close()

asyncio.run(run())
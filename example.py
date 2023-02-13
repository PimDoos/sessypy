import asyncio
from sessypy.api import SessyApi
from sessypy.const import SessyApiCommand
from config import * # Hide your secrets here

async def run():
    print("P1 Status")
    p1_api = SessyApi(SESSY_P1_HOST, SESSY_P1_USERNAME, SESSY_P1_PASSWORD)
    result = await p1_api.get(SessyApiCommand.P1_STATUS)
    print(result)
    await p1_api.close()
    print("")

    print("Power Status")
    battery_api = SessyApi(SESSY_BATTERY_HOST, SESSY_BATTERY_USERNAME, SESSY_BATTERY_PASSWORD)
    result = await battery_api.get(SessyApiCommand.POWER_STATUS)
    print(result)
    print("")

    print("Power Strategy")
    result = await battery_api.get(SessyApiCommand.POWER_STRATEGY)
    print(result)
    print("")
    
    await battery_api.close()

asyncio.run(run())
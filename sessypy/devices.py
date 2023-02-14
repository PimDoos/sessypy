from .const import SessyApiCommand
from .api import SessyApi

class SessyDevice():
    def __init__(self, host, username: str, password: str):
        self.api = SessyApi(host, username, password)

    async def close(self):
        await self.api.close()
    
class SessyBattery(SessyDevice):
    async def get_power_status(self):
        return await self.api.get(SessyApiCommand.POWER_STATUS)
    
    async def get_power_strategy(self):
        return await self.api.get(SessyApiCommand.POWER_STRATEGY)

class SessyP1Meter(SessyDevice):
    async def get_p1_status(self):
        return await self.api.get(SessyApiCommand.P1_STATUS)
    
	
        
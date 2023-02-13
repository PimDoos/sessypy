from .const import SessyApiCommand
from .api import SessyApi

class SessyBattery():
    def __init__(self, api: SessyApi):
        self.api = api

    async def get_power_status(self):
        return await self.api.get(SessyApiCommand.POWER_STATUS)
    
    async def get_power_strategy(self):
        return await self.api.get(SessyApiCommand.POWER_STRATEGY)

class SessyP1Meter():
    def __init__(self, api: SessyApi):
        self.api = api

    async def get_p1_status(self):
        return await self.api.get(SessyApiCommand.P1_STATUS)
    
	
        
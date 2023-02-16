from .const import SessyApiCommand, SessyPowerStrategy
from .api import SessyApi

class SessyDevice():
    def __init__(self, host, username: str, password: str):
        self.api = SessyApi(host, username, password)
        self.host = host
    
    async def test(self):
        return await self.api.get()

    async def get_ota_status(self):
        return await self.api.get(SessyApiCommand.OTA_STATUS)   
    
    async def get_network_status(self):
        return await self.api.get(SessyApiCommand.NETWORK_STATUS)   

    async def close(self):
        await self.api.close()
    
class SessyBattery(SessyDevice):
    async def get_power_status(self):
        return await self.api.get(SessyApiCommand.POWER_STATUS)
    
    async def set_power_setpoint(self, setpoint: int):
        return await self.api.post(SessyApiCommand.POWER_SETPOINT, {"setpoint": setpoint})
    
    async def get_power_strategy(self):
        return await self.api.get(SessyApiCommand.POWER_STRATEGY)
    
    async def set_power_strategy(self, strategy: SessyPowerStrategy):
        return await self.api.post(SessyApiCommand.POWER_STRATEGY, {"strategy": strategy.value})

    async def get_system_settings(self):
        return await self.api.get(SessyApiCommand.SYSTEM_SETTINGS)

class SessyP1Meter(SessyDevice):
    async def get_p1_status(self):
        return await self.api.get(SessyApiCommand.P1_STATUS)
    
	
        
from .const import SessyApiCommand, SessyOtaTarget, SessyPowerStrategy
from .api import SessyApi
from .util import SessyConnectionException, SessyNotSupportedException

class SessyDevice():
    def __init__(self, host, username: str, password: str):
        self._serial_number = username.upper()
        self.api = SessyApi(host, username, password)
        self.host = host
    
    def __init__(self, api: SessyApi):
        self._serial_number = api.username.upper()
        self.api = api
        self.host = api.host

    @property
    def serial_number(self):
        return self._serial_number
    
    @property
    def name(self):
        return f"Sessy-{ self.serial_number[0:4] }"

    async def get_ota_status(self):
        return await self.api.get(SessyApiCommand.OTA_STATUS)
    
    async def check_ota(self):
        return await self.api.get(SessyApiCommand.OTA_CHECK)
    
    async def install_ota(self, target: SessyOtaTarget):
        return await self.api.post(SessyApiCommand.OTA_START, {"target": target.value})
    
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

class SessyCTMeter(SessyDevice):
    pass    
	

"""Connect to the API and determine the device type"""
async def get_sessy_device(host: str, username: str, password: str) -> SessyDevice:

    device_profiles = [
        (SessyBattery, SessyApiCommand.POWER_STRATEGY),
        (SessyP1Meter, SessyApiCommand.P1_STATUS),
        #(SessyDevice, SessyApiCommand.NETWORK_STATUS),
    ]

    api = SessyApi(host, username, password)

    for device_profile in device_profiles:
        try:
            await api.get(device_profile[1])
            return device_profile[0](api)
        except SessyConnectionException:
            pass
        except SessyNotSupportedException:
            pass

    return None
        
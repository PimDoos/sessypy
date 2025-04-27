from .const import SessyApiCommand, SessyOtaTarget, SessyPowerStrategy
from .api import SessyApi
from .util import SessyConnectionException, SessyNotSupportedException
import logging

_LOGGER = logging.getLogger(__name__)

class SessyDevice():
    def __init__(self, host, username: str, password: str):
        self._serial_number = username.upper()
        self._api = SessyApi(host, username, password)
        self._host = host
    
    def __init__(self, api: SessyApi):
        self._serial_number = api.username.upper()
        self._api = api
        self._host = api.host

    @property
    def serial_number(self) -> str:
        return self._serial_number
    
    @property
    def name(self) -> str:
        return f"Sessy-{ self.serial_number[0:4] }"
    
    @property
    def host(self) -> str:
        return self._host

    @property
    def api(self) -> SessyApi:
        return self._api

    async def get_ota_status(self):
        return await self.api.get(SessyApiCommand.OTA_STATUS)
    
    async def check_ota(self):
        return await self.api.get(SessyApiCommand.OTA_CHECK)
    
    async def install_ota(self, target: SessyOtaTarget):
        return await self.api.post(SessyApiCommand.OTA_START, {"target": target.value})
    
    async def get_network_scan(self):
        return await self.api.get(SessyApiCommand.NETWORK_SCAN)
    
    async def get_network_status(self):
        return await self.api.get(SessyApiCommand.NETWORK_STATUS)
    
    async def get_system_info(self):
        return await self.api.get(SessyApiCommand.SYSTEM_INFO)
    
    async def restart(self):
        return await self.api.post(SessyApiCommand.SYSTEM_RESTART)

    async def set_wifi_credentials(self, ssid: str, password: str):
        return await self.api.post(SessyApiCommand.WIFI_STA_CREDENTIALS, {"ssid":ssid, "pass":password})

    async def close(self):
        await self.api.close()
    
class SessyBattery(SessyDevice):
    async def get_dynamic_schedule(self):
        return await self.api.get(SessyApiCommand.DYNAMIC_SCHEDULE)
    
    async def get_energy_status(self):
        return await self.api.get(SessyApiCommand.ENERGY_STATUS)
    
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
    
    async def set_system_settings(self, settings):
        return await self.api.post(SessyApiCommand.SYSTEM_SETTINGS, settings)
    
    async def set_system_setting(self, key, value):
        settings = await self.get_system_settings()
        settings[key] = value
        return await self.set_system_settings(settings)
    
class SessyMeter(SessyDevice):
    async def get_grid_target(self):
        return await self.api.get(SessyApiCommand.METER_GRID_TARGET)
    
    async def set_grid_target(self, grid_target: int):
        return await self.api.post(SessyApiCommand.METER_GRID_TARGET, {"grid_target": grid_target})
    
    async def get_meter_status(self):
        return await self.api.get(SessyApiCommand.METER_STATUS)

class SessyP1Meter(SessyMeter):
    async def get_p1_details(self):
        return await self.api.get(SessyApiCommand.P1_DETAILS)

class SessyCTMeter(SessyMeter):
    async def get_ct_details(self):
        return await self.api.get(SessyApiCommand.CT_DETAILS)
    
    async def get_energy_status(self):
        return await self.api.get(SessyApiCommand.ENERGY_STATUS)
	

"""Connect to the API and determine the device type"""
async def get_sessy_device(host: str, username: str, password: str) -> SessyDevice:
    # Assume username == serial number, which is mostly correct
    serial_number = username

    # Identify devices by API call and first letter of serial number
    device_profiles = [
        (SessyBattery, SessyApiCommand.POWER_STRATEGY, "D"),
        (SessyP1Meter, SessyApiCommand.P1_DETAILS, "P"),
        (SessyCTMeter, SessyApiCommand.CT_DETAILS, "C"),
    ]

    api = SessyApi(host, username, password)

    for device_profile in device_profiles:
        if serial_number[0].upper() != device_profile[2]:
            continue
        try:
            await api.get(device_profile[1])
            _LOGGER.debug(f"Found matching profile {device_profile[0]} for {host}")
            return device_profile[0](api)
        except SessyConnectionException:
            _LOGGER.debug(f"Skipping device profile {device_profile[0]} for {host}: Connection exception")

        except SessyNotSupportedException:
            _LOGGER.debug(f"Skipping device profile {device_profile[0]} for {host}: Not supported")


    await api.close()
    
    # Device does not match any known device profiles, so it is not supported
    raise SessyNotSupportedException

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
    
    async def get_dynamic_schedule_legacy(self):
        return await self.api.get(SessyApiCommand.DYNAMIC_SCHEDULE_LEGACY)
    
    async def get_energy_status(self):
        return await self.api.get(SessyApiCommand.ENERGY_STATUS)
    
    async def get_power_status(self):
        return await self.api.get(SessyApiCommand.POWER_STATUS)
    
    async def set_power_setpoint(self, setpoint: int):
        return await self.api.post(SessyApiCommand.POWER_SETPOINT, {"setpoint": setpoint})
    
    async def get_power_strategy(self):
        return await self.api.get(SessyApiCommand.POWER_STRATEGY)
    
    async def set_power_strategy(self, strategy: SessyPowerStrategy):
        return await self.api.post(SessyApiCommand.POWER_STRATEGY, {"strategy": strategy})

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

    DEVICE_TYPE_LOOKUP = {
        "A": None, # AC Board has no API
        "C": SessyCTMeter,
        "D": SessyBattery,
        "P": SessyP1Meter,
    }

    # Setup the API connection
    api = SessyApi(host, username, password)

    # Fetch the system info API to determine the device type
    try:
        system_info: dict = await api.get(SessyApiCommand.SYSTEM_INFO)
        _LOGGER.debug(f"System info for {host}: {system_info}")
    except SessyConnectionException as e:
        _LOGGER.error(f"Failed to connect to {host}: {e}")
        raise SessyConnectionException from e
    except SessyNotSupportedException as e:
        _LOGGER.error(f"Device at {host} is not supported: {e}")
        raise SessyNotSupportedException from e
    

    serial_number = system_info.get("self_serial")

    if not serial_number or serial_number == "unknown":
        if username:
            _LOGGER.debug(f"Failed to detect serial number for device at '{host}', using username '{username}' as serial number")
            serial_number = username.upper()
        else:
            _LOGGER.error(f"Discovery failed: Could not get the serial number for '{host}'")
            await api.close()
            raise SessyNotSupportedException(f"Could not get the serial number for '{host}'")
    
    model_id = serial_number[0].upper() if serial_number else None

    if DEVICE_TYPE_LOOKUP.get(model_id) is None:
        _LOGGER.error(f"Unknown device type '{model_id}' at '{host}' with serial number '{serial_number}' is not supported")
        await api.close()
        raise SessyNotSupportedException(f"Unknown device type '{model_id}' at '{host}' with serial number '{serial_number}' is not supported")
    else:
        device_class = DEVICE_TYPE_LOOKUP[model_id]

    if device_class:
        _LOGGER.debug(f"Creating device instance for {device_class.__name__} with serial number {serial_number}")
        return device_class(api)
    else:
        _LOGGER.debug(f"Device at {host} with serial number {serial_number} does not match any known device profiles")
        # Close the API connection before raising the exception
        await api.close()
    
        # Device does not match any known device profiles, so it is not supported
        raise SessyNotSupportedException(f"Device at {host} with serial number {serial_number} does not match any known device profiles")

    

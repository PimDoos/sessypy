from enum import Enum

API_VERSION_1 = "api/v1"

class SessyApiCommand(str, Enum):
    NETWORK_STATUS = f"{API_VERSION_1}/network/status"
    OTA_STATUS = f"{API_VERSION_1}/ota/status"
    POWER_SETPOINT = f"{API_VERSION_1}/power/setpoint"
    POWER_STATUS = f"{API_VERSION_1}/power/status"
    POWER_STRATEGY = f"{API_VERSION_1}/power/active_strategy"
    P1_STATUS = f"{API_VERSION_1}/p1/status"
    SYSTEM_SETTINGS = f"{API_VERSION_1}/system/settings"
    

SESSY_DEVICE = "sessy_device"
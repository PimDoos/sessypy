from enum import Enum

API_VERSION_1 = "api/v1"

class SessyApiCommand(str, Enum):
    POWER_STATUS = f"{API_VERSION_1}/power/status"
    POWER_STRATEGY = f"{API_VERSION_1}/power/active_strategy"
    P1_STATUS = f"{API_VERSION_1}/p1/status"
    

SESSY_DEVICE = "sessy_device"
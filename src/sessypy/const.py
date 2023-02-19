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

class SessyPowerStrategy(str, Enum):
    API = "POWER_STRATEGY_API"
    NOM = "POWER_STRATEGY_NOM"
    ROI = "POWER_STRATEGY_ROI"
    IDLE = "POWER_STRATEGY_IDLE"

class SessySystemState(str, Enum):
    RUNNING_SAFE = "SYSTEM_STATE_RUNNING_SAFE"
    STANDBY = "SYSTEM_STATE_STANDBY"
    WAITING_SAFE = "SYSTEM_STATE_WAITING_IN_SAFE_STATE"
    ERROR = "SYSTEM_STATE_ERROR"

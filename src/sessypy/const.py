from enum import Enum

API_VERSION_1 = "api/v1"

class SessyApiCommand(str, Enum):
    NETWORK_STATUS = f"{API_VERSION_1}/network/status"
    OTA_CHECK = f"{API_VERSION_1}/ota/check"
    OTA_START = f"{API_VERSION_1}/ota/start"
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
    WAITING_SAFE = "SYSTEM_STATE_WAITING_IN_SAFE_SITUATION"
    WAITING_PERIPHERALS = "SYSTEM_STATE_WAIT_FOR_PERIPHERALS"
    ERROR = "SYSTEM_STATE_ERROR"

class SessyP1State(str, Enum):
    NOT_CONNECTED = "P1_NOT_CONNECTED"
    DATA_VALIDITY_ERROR = "P1_DATAVALIDITY_ERR"
    VERSION_ERROR = "P1_VERSION_ERR"
    PARSE_ERROR = "P1_PARSE_ERR"
    OK = "P1_OK"

class SessyOtaTarget(str, Enum):
    SELF = "OTA_TARGET_SELF"
    SERIAL = "OTA_TARGET_SERIAL"

class SessyOtaState(str, Enum):
    FAILED = "OTA_UPDATE_FAILED"
    INACTIVE = "OTA_INACTIVE"
    CHECKING = "OTA_CHECKING"
    CHECK_FAILED = "OTA_CHECK_FAILED"
    UP_TO_DATE = "OTA_UP_TO_DATE"
    AVAILABLE = "OTA_NEW_VERSION_AVAILABLE"
    UPDATING = "OTA_UPDATING"
    DONE = "OTA_DONE"
    UNKNOWN = "unknown"
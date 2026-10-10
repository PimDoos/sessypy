"""Typed response models for Sessy API payloads.

The models in this module describe the JSON payloads returned by the
Sessy Dongle (D) and P1 meter (P) APIs documented in the project docs.
"""

from typing import Literal, NotRequired, TypedDict

from .const import SessyModbusState, SessyP1State, SessyPowerStrategy, SessySystemState


class SessyPhase(TypedDict):
    """Single phase grid/renewable power data."""

    voltage_rms: float
    current_rms: float
    power: int


class SessyPowerStatusDevice(TypedDict):
    """Status object returned by /api/v1/power/status."""

    state_of_charge: float
    power: int
    external_power: int
    pack_voltage: int
    power_setpoint: int
    system_state: SessySystemState
    system_state_details: str
    frequency: int
    inverter_current_ma: int
    strategy_overridden: bool


class SessyPowerStatus(TypedDict):
    """Full Dongle power status payload."""

    sessy: SessyPowerStatusDevice
    renewable_energy_phase1: SessyPhase
    renewable_energy_phase2: SessyPhase
    renewable_energy_phase3: SessyPhase


class SessyActivePowerStrategy(TypedDict):
    """Active power strategy response."""

    strategy: SessyPowerStrategy
    status: NotRequired[str]


class SessyPowerSetpoint(TypedDict):
    """Setpoint payload for /api/v1/power/setpoint."""

    setpoint: int


class SessyEnergyValue(TypedDict):
    """Import/export energy totals for a device or phase."""

    import_wh: float
    export_wh: float


class SessyEnergyStatus(TypedDict):
    """Energy meter totals returned by /api/v1/energy/status."""

    sessy_energy: SessyEnergyValue
    energy_phase1: SessyEnergyValue
    energy_phase2: SessyEnergyValue
    energy_phase3: SessyEnergyValue


class SessyDynamicScheduleEntry(TypedDict):
    """Scheduled power slot from the dynamic schedule API."""

    start_time: int
    end_time: int
    power: int


class SessyEnergyPrice(TypedDict):
    """Price slot from the dynamic schedule API."""

    start_time: int
    end_time: int
    price: int


class SessyDynamicSchedule(TypedDict):
    """Dynamic schedule payload from /api/v2/dynamic/schedule."""

    dynamic_schedule: list[SessyDynamicScheduleEntry] | None
    energy_prices: list[SessyEnergyPrice] | None


class ModbusPhaseDetails(TypedDict):
    """Modbus meter data for a single phase."""

    voltage: float
    current: float
    power: float


class ModbusDetails(TypedDict):
    """Payload returned by /api/v1/modbus/details."""

    status: str
    phase_1: ModbusPhaseDetails
    phase_2: ModbusPhaseDetails
    phase_3: ModbusPhaseDetails
    total_power: float
    total_import: float
    total_export: float
    device_type: str
    device_uid: str
    time_since: float
    state: SessyModbusState


class P1Details(TypedDict):
    """Payload returned by /api/v2/p1/details."""

    status: str
    state: SessyP1State
    dsmr_version: int
    header_info: str
    equipment_identifier: str
    date_time: str
    power_consumed_tariff1: float
    power_produced_tariff1: float
    power_consumed_tariff2: float
    power_produced_tariff2: float
    tariff_indicator: int
    power_consumed: float
    power_produced: float
    power_total: float
    power_failure_any_phase: int
    long_power_failure_any_phase: int
    voltage_sag_count_l1: int
    voltage_sag_count_l2: int
    voltage_sag_count_l3: int
    voltage_swell_count_l1: int
    voltage_swell_count_l2: int
    voltage_swell_count_l3: int
    voltage_l1: float
    voltage_l2: float
    voltage_l3: float
    current_l1: float
    current_l2: float
    current_l3: float
    power_consumed_l1: float
    power_consumed_l2: float
    power_consumed_l3: float
    power_produced_l1: float
    power_produced_l2: float
    power_produced_l3: float
    gas_meter_equipment_identifier: str
    gas_meter_value_time: str
    gas_meter_value: float


class GridTargetGet(TypedDict):
    """Grid target response returned by GET /api/v1/meter/grid_target."""

    status: str
    grid_target: int


class GridTargetSet(TypedDict):
    """Grid target payload used by POST /api/v1/meter/grid_target."""

    grid_target: int


class ApiOkResponse(TypedDict):
    """Generic success response returned by several API endpoints."""

    status: Literal["ok"]


__all__ = [
    "ApiOkResponse",
    "GridTargetGet",
    "GridTargetSet",
    "ModbusDetails",
    "ModbusPhaseDetails",
    "P1Details",
    "SessyActivePowerStrategy",
    "SessyDynamicSchedule",
    "SessyDynamicScheduleEntry",
    "SessyEnergyPrice",
    "SessyEnergyStatus",
    "SessyEnergyValue",
    "SessyPhase",
    "SessyPowerSetpoint",
    "SessyPowerStatus",
    "SessyPowerStatusDevice",
]

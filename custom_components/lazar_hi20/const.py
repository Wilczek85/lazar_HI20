"""Constants for the HKS Lazar integration."""
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    PERCENTAGE,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

DOMAIN = "lazar_hi20"
CONF_ROOM_SENSOR = "room_sensor"
DEFAULT_NAME = "Pompa Ciepła Lazar"

BASE_URL = "https://hkslazar.net"
LOGIN_URL = f"{BASE_URL}/sollogin"
DATA_URL = f"{BASE_URL}/oemSerwis?what=bcst"
SET_URL = f"{BASE_URL}/oemSerwis?what=setparam"

# Dodano ikony (mdi:...) do definicji
SENSOR_TYPES = {
    "temp_zew": {"path": "stat.temps.zew", "unit": UnitOfTemperature.CELSIUS, "class": SensorDeviceClass.TEMPERATURE, "scale": 0.1, "name": "Temperatura zewnętrzna"},
    "temp_out": {"path": "stat.temps.out", "unit": UnitOfTemperature.CELSIUS, "class": SensorDeviceClass.TEMPERATURE, "scale": 0.1, "name": "Temperatura powietrza wylot"},
    "temp_ret": {"path": "stat.temps.ret", "unit": UnitOfTemperature.CELSIUS, "class": SensorDeviceClass.TEMPERATURE, "scale": 0.1, "name": "Temperatura powrotu CO"},
    "temp_cwu": {"path": "stat.temps.cwu", "unit": UnitOfTemperature.CELSIUS, "class": SensorDeviceClass.TEMPERATURE, "scale": 0.1, "name": "Temperatura CWU"},
    "fan_speed": {"path": "stat.unit.fan", "unit": PERCENTAGE, "name": "Prędkość wentylatora", "icon": "mdi:fan"},
    "compr_power": {"path": "stat.unit.comprpow", "unit": UnitOfPower.WATT, "class": SensorDeviceClass.POWER, "name": "Moc sprężarki"},
    "powerneed": {"path": "stat.unit.powerneed", "unit": UnitOfPower.WATT, "class": SensorDeviceClass.POWER, "name": "Pobór mocy całkowity"},
    "eevheat": {"path": "stat.unit.eevheat", "unit": PERCENTAGE, "name": "Pozycja EEV – grzanie", "icon": "mdi:gauge"},
    "eevcool": {"path": "stat.unit.eevcool", "unit": PERCENTAGE, "name": "Pozycja EEV – chłodzenie", "icon": "mdi:gauge"},
    "pump_cir1": {"path": "stat.pumps.pumpcir1", "name": "Pompa obiegowa 1", "icon": "mdi:pump"},
    "pump_cir2": {"path": "stat.pumps.pumpcir2", "name": "Pompa obiegowa 2", "icon": "mdi:pump"},
    "heater_leak": {"path": "stat.heaters.leak", "name": "Czujnik wycieku", "icon": "mdi:water-alert"},
    "heater_flow1": {"path": "stat.heaters.flowlvl1", "name": "Poziom przepływu CO 1", "icon": "mdi:pipe-valve"},
    "heater_flow2": {"path": "stat.heaters.flowlvl2", "name": "Poziom przepływu CO 2", "icon": "mdi:pipe-valve"},
    "heater_carter": {"path": "stat.heaters.carter", "name": "Czujnik carter"},
    "troomsetheat": {"path": "params.cricuits.0.troomsetheat", "name": "Temperatura pokojowa (odczyt)", "unit": UnitOfTemperature.CELSIUS, "class": SensorDeviceClass.TEMPERATURE},
    "alarm_count": {"path": "stat.alarmcnt", "name": "Liczba alarmów", "icon": "mdi:alert-circle-outline"},
}

NUMBER_TYPES = {
    "tseteco": {"path": "params.cwu.tseteco", "unit": UnitOfTemperature.CELSIUS, "scale": 0.1, "name": "CWU ECO", "min": 20, "max": 60, "step": 1, "icon": "mdi:water-thermometer"},
    "tsetcomf": {"path": "params.cwu.tsetcomf", "unit": UnitOfTemperature.CELSIUS, "scale": 0.1, "name": "CWU Komfort", "min": 20, "max": 60, "step": 1, "icon": "mdi:water-thermometer"},
    "tsetcrvTp15": {"path": "params.cricuits.0.tsetcrvTp15", "unit": UnitOfTemperature.CELSIUS, "scale": 0.1, "name": "Krzywa +15", "min": 20, "max": 60, "step": 1, "icon": "mdi:chart-bell-curve"},
    "tsetcrvT0": {"path": "params.cricuits.0.tsetcrvT0", "unit": UnitOfTemperature.CELSIUS, "scale": 0.1, "name": "Krzywa 0", "min": 20, "max": 60, "step": 1, "icon": "mdi:chart-bell-curve"},
    "tsetcrvTm10": {"path": "params.cricuits.0.tsetcrvTm10", "unit": UnitOfTemperature.CELSIUS, "scale": 0.1, "name": "Krzywa -10", "min": 20, "max": 60, "step": 1, "icon": "mdi:chart-bell-curve"},
    "tsetcrvTm20": {"path": "params.cricuits.0.tsetcrvTm20", "unit": UnitOfTemperature.CELSIUS, "scale": 0.1, "name": "Krzywa -20", "min": 20, "max": 60, "step": 1, "icon": "mdi:chart-bell-curve"},
}

SELECT_TYPES = {
    "mode": {"path": "params.mode", "name": "Tryb pracy", "options": ["Grzanie (CO)", "Chłodzenie", "CWU"], "icon": "mdi:hvac"},
}

SWITCH_TYPES = {
    # Tutaj przypisujemy główną ikonę pompy ciepła
    "onoff": {"path": "params.onoff", "name": "Pompa Włącz/Wyłącz", "icon": "mdi:heat-pump"},
}
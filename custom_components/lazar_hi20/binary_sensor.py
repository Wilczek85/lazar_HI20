from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, DEFAULT_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LazarBinarySensor(coordinator)])

class LazarBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = f"{DEFAULT_NAME} Alarm"
        self._attr_unique_id = "lazar_alarm_active"
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def is_on(self):
        # Path: stat.alarmcnt
        cnt = self.coordinator.data.get("stat", {}).get("alarmcnt", 0)
        return cnt > 0

    @property
    def extra_state_attributes(self):
        return {
            "alarms_list": self.coordinator.data.get("stat", {}).get("alarms", [])
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "main_unit")},
            "name": DEFAULT_NAME,
        }
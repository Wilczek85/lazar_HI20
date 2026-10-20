from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSOR_TYPES, DEFAULT_NAME
from .coordinator import get_value_from_path
from .values import numeric_value
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for key, cfg in SENSOR_TYPES.items():
        entities.append(LazarSensor(coordinator, key, cfg))
    async_add_entities(entities)

class LazarSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, cfg):
        super().__init__(coordinator)
        self.key = key
        self.cfg = cfg
        self._attr_name = f"{DEFAULT_NAME} {cfg['name']}"
        self._attr_unique_id = f"lazar_{key}"
        self._attr_native_unit_of_measurement = cfg.get("unit")
        self._attr_device_class = cfg.get("class")
        self._attr_icon = cfg.get("icon")
        if cfg.get("unit") is not None and key != "room_target_heat":
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if cfg.get("class") == "temperature":
            self._attr_suggested_display_precision = 1

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        source = self.coordinator.room_sensor_entity
        if self.cfg.get("source") == "room" and source:
            self.async_on_remove(async_track_state_change_event(
                self.hass, [source], self._room_changed
            ))

    @callback
    def _room_changed(self, event):
        self.async_write_ha_state()

    @property
    def available(self):
        if self.cfg.get("source") == "room":
            return self.coordinator.room_temperature is not None
        return super().available and self.native_value is not None

    @property
    def native_value(self):
        if self.cfg.get("source") == "room":
            return self.coordinator.room_temperature
        raw = get_value_from_path(self.coordinator.data, self.cfg["path"])
        return numeric_value(raw, self.cfg.get("scale", 1))

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "main_unit")},
            "name": DEFAULT_NAME,
            "manufacturer": "HKS Lazar",
        }
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSOR_TYPES, DEFAULT_NAME
from .coordinator import get_value_from_path

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

    @property
    def native_value(self):
        raw = get_value_from_path(self.coordinator.data, self.cfg["path"])
        if raw is None or raw == -9999:
            return None
        scale = self.cfg.get("scale", 1)
        return raw * scale

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "main_unit")},
            "name": DEFAULT_NAME,
            "manufacturer": "HKS Lazar",
        }
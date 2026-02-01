from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NUMBER_TYPES, DEFAULT_NAME
from .coordinator import get_value_from_path
from homeassistant.const import EntityCategory, UnitOfTemperature
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for key, cfg in NUMBER_TYPES.items():
        entities.append(LazarNumber(coordinator, key, cfg))
    async_add_entities(entities)

class LazarNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, key, cfg):
        super().__init__(coordinator)
        self.key = key
        self.cfg = cfg
        self._attr_name = f"{DEFAULT_NAME} {cfg['name']}"
        self._attr_unique_id = f"lazar_{key}"
        self._attr_native_min_value = cfg["min"]
        self._attr_native_max_value = cfg["max"]
        self._attr_native_step = cfg["step"]
        self._attr_native_unit_of_measurement = cfg.get("unit")
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_icon = cfg.get("icon")
        
        # Ustawienie klasy urządzenia (np. Temperatura) poprawia wygląd w GUI
        if cfg.get("unit") == UnitOfTemperature.CELSIUS:
            self._attr_device_class = NumberDeviceClass.TEMPERATURE

    @property
    def native_value(self):
        raw = get_value_from_path(self.coordinator.data, self.cfg["path"])
        if raw is None: return None
        return raw * self.cfg.get("scale", 1)

    async def async_set_native_value(self, value: float) -> None:
        to_send = value
        if self.cfg.get("scale") == 0.1:
            to_send = int(value * 10)
            
        _LOGGER.debug("Ustawianie %s na %s (wysyłane: %s)", self.key, value, to_send)
        await self.coordinator.set_param(self.key, to_send)

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "main_unit")}, "name": DEFAULT_NAME}
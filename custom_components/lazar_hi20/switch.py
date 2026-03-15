from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SWITCH_TYPES, DEFAULT_NAME
from .coordinator import get_value_from_path

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    for key, cfg in SWITCH_TYPES.items():
        async_add_entities([LazarSwitch(coordinator, key, cfg)])

class LazarSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, key, cfg):
        super().__init__(coordinator)
        self.key = key
        self.cfg = cfg
        self._attr_name = f"{DEFAULT_NAME} {cfg['name']}"
        self._attr_unique_id = f"lazar_{key}"
        self._attr_icon = cfg.get("icon")
        self._optimistic_state = None  # Flaga do optymistycznego stanu

    @property
    def is_on(self):
        """Zwraca stan, priorytetyzując optymistyczną wartość w trakcie odświeżania."""
        if self._optimistic_state is not None:
            return self._optimistic_state
        val = get_value_from_path(self.coordinator.data, self.cfg["path"])
        return val == 1

    async def async_turn_on(self, **kwargs):
        self._optimistic_state = True
        self.async_write_ha_state() # Natychmiastowa aktualizacja interfejsu
        try:
            await self.coordinator.set_param(self.key, 1)
        finally:
            self._optimistic_state = None # Czyszczenie flagi, gdy API zakończy lub zaktualizuje dane

    async def async_turn_off(self, **kwargs):
        self._optimistic_state = False
        self.async_write_ha_state()
        try:
            await self.coordinator.set_param(self.key, 0)
        finally:
            self._optimistic_state = None

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "main_unit")}, "name": DEFAULT_NAME}

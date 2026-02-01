from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SELECT_TYPES, DEFAULT_NAME
from .coordinator import get_value_from_path
from homeassistant.const import EntityCategory

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for key, cfg in SELECT_TYPES.items():
        entities.append(LazarSelect(coordinator, key, cfg))
    async_add_entities(entities)

class LazarSelect(CoordinatorEntity, SelectEntity):
    def __init__(self, coordinator, key, cfg):
        super().__init__(coordinator)
        self.key = key
        self.cfg = cfg
        self._attr_name = f"{DEFAULT_NAME} {cfg['name']}"
        self._attr_unique_id = f"lazar_{key}"
        self._attr_options = cfg["options"]
        self._attr_entity_category = EntityCategory.CONFIG
        # Dodano obsługę ikony z konfiguracji
        self._attr_icon = cfg.get("icon")

    @property
    def current_option(self):
        raw = get_value_from_path(self.coordinator.data, self.cfg["path"])
        if raw is None: return None
        try:
            idx = int(raw)
            if 0 <= idx < len(self._attr_options):
                return self._attr_options[idx]
            else:
                return None
        except (IndexError, ValueError):
            return None

    @property
    def extra_state_attributes(self):
        raw = get_value_from_path(self.coordinator.data, self.cfg["path"])
        return {
            "raw_value": raw,
            "api_path": self.cfg["path"]
        }

    async def async_select_option(self, option: str) -> None:
        idx = self._attr_options.index(option)
        await self.coordinator.set_param(self.key, idx)

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "main_unit")}, "name": DEFAULT_NAME}
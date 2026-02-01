from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([LazarClimate()])

class LazarClimate(ClimateEntity):
    name = "Lazar HI20 Climate"
    hvac_modes = [HVACMode.HEAT]
    hvac_mode = HVACMode.HEAT
    temperature_unit = "°C"

    @property
    def current_temperature(self):
        return None
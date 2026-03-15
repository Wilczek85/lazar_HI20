from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from .const import DOMAIN, DEFAULT_NAME
from .coordinator import get_value_from_path

async def async_setup_entry(hass, entry, async_add_entities):
    # Przekazujemy koordynatora do encji
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LazarClimate(coordinator)])

class LazarClimate(CoordinatorEntity, ClimateEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = f"{DEFAULT_NAME} Termostat"
        self._attr_unique_id = "lazar_climate_main"
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        # Definiujemy wspierane tryby
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        # Wsparcie dla włącz/wyłącz oraz ustawiania temperatury
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | 
            ClimateEntityFeature.TURN_ON | 
            ClimateEntityFeature.TURN_OFF
        )
        self._enable_turn_on_off_backwards_compatibility = False

    @property
    def hvac_mode(self):
        """Zwraca obecny tryb pompy."""
        is_on = get_value_from_path(self.coordinator.data, "params.onoff")
        if not is_on:
            return HVACMode.OFF
        return HVACMode.HEAT

    @property
    def current_temperature(self):
        """Zwraca aktualną temperaturę (np. powrót CO). Możesz to zmienić na inny odpowiedni czujnik."""
        val = get_value_from_path(self.coordinator.data, "stat.temps.ret")
        return val * 0.1 if val is not None else None

    @property
    def target_temperature(self):
        """Zwraca zadaną temperaturę pokojową z obiegu pierwszego."""
        val = get_value_from_path(self.coordinator.data, "params.cricuits.0.troomsetheat")
        return val * 0.1 if val is not None else None

    async def async_set_temperature(self, **kwargs):
        """Ustawienie temperatury docelowej."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            # W API prawdopodobnie ustawiamy wartość przemnożoną przez 10
            await self.coordinator.set_param("troomsetheat", int(temp * 10))

    async def async_set_hvac_mode(self, hvac_mode):
        """Włączanie lub wyłączanie pompy."""
        if hvac_mode == HVACMode.OFF:
            await self.coordinator.set_param("onoff", 0)
        else:
            await self.coordinator.set_param("onoff", 1)
            
    @property
    def device_info(self):
        """Grupowanie w jednym urządzeniu."""
        return {"identifiers": {(DOMAIN, "main_unit")}, "name": DEFAULT_NAME}

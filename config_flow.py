"""Config flow for HKS Lazar."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.core import callback
import logging

from .const import DOMAIN, CONF_ROOM_SENSOR
from .coordinator import LazarCoordinator

_LOGGER = logging.getLogger(__name__)

class LazarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HKS Lazar."""
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LazarOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}
        
        if user_input is not None:
            # Validate login by trying to instantiate coordinator and login
            try:
                # Temporary coordinator for validation
                coord = LazarCoordinator(self.hass, user_input)
                await coord._login()
                await coord.close()
                
                return self.async_create_entry(
                    title=f"Lazar ({user_input['username']})",
                    data=user_input
                )
            except Exception as e:
                _LOGGER.error("Błąd logowania: %s", e)
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Optional(CONF_ROOM_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

class LazarOptionsFlowHandler(config_entries.OptionsFlow):
    """Obsługa zmiany opcji (Konfiguruj) po instalacji."""

    def __init__(self, config_entry):
        # Zmieniono nazwę zmiennej z self.config_entry na self.entry
        # aby uniknąć konfliktu z wbudowaną właściwością (read-only property)
        self.entry = config_entry

    async def async_step_init(self, user_input=None):
        """Zarządzaj opcjami."""
        if user_input is not None:
            # Zapisz nowe opcje
            return self.async_create_entry(title="", data=user_input)

        # Pobierz aktualnie ustawiony czujnik (z opcji lub z konfiguracji początkowej)
        # Używamy tutaj self.entry zamiast self.config_entry
        current_sensor = self.entry.options.get(
            CONF_ROOM_SENSOR, 
            self.entry.data.get(CONF_ROOM_SENSOR)
        )

        schema = vol.Schema({
            vol.Optional(CONF_ROOM_SENSOR, description={"suggested_value": current_sensor}): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
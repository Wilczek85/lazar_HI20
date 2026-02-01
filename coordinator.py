"""DataUpdateCoordinator for HKS Lazar."""
import logging
import aiohttp
import asyncio
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN, LOGIN_URL, DATA_URL, SET_URL, CONF_ROOM_SENSOR

_LOGGER = logging.getLogger(__name__)

class LazarCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, entry_data):
        """Initialize."""
        self.hass = hass
        self.username = entry_data["username"]
        self.password = entry_data["password"]
        self.room_sensor_entity = entry_data.get(CONF_ROOM_SENSOR)
        # Używamy cookie_jar unsafe=True, aby akceptować ciastka IP/domen lokalnych bez problemów
        self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True))
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Update data via library with retry logic."""
        # Próba 1: Normalne pobranie (może użyć istniejącej sesji)
        try:
            return await self._fetch_and_parse()
        except (ConfigEntryAuthFailed, aiohttp.ClientError, ValueError) as err:
            _LOGGER.warning("Błąd pobierania danych (próba 1), próba odnowienia sesji: %s", err)
            # Próba 2: Wymuszone logowanie i ponowne pobranie
            try:
                await self._login()
                return await self._fetch_and_parse()
            except Exception as retry_err:
                raise UpdateFailed(f"Błąd komunikacji z API po przelogowaniu: {retry_err}")

    async def _fetch_and_parse(self):
        """Internal method to fetch data."""
        # Jeśli nie mamy ciastka w ogóle, zaloguj się
        if not self._has_valid_cookie():
            await self._login()

        async with self.session.get(DATA_URL, timeout=10) as resp:
            resp.raise_for_status()
            
            # Weryfikacja czy dostaliśmy JSON (jeśli sesja wygasła, serwer może zwrócić HTML z logowaniem)
            if "application/json" not in resp.headers.get("Content-Type", ""):
                # To rzuci wyjątek, który złapiemy w _async_update_data i wymusimy re-login
                raise ConfigEntryAuthFailed("Otrzymano niepoprawny format danych (prawdopodobnie wygasła sesja).")
                
            data = await resp.json()

        # Logika czujnika pokojowego (bez zmian)
        if self.room_sensor_entity:
            state = self.hass.states.get(self.room_sensor_entity)
            if state and state.state not in ["unknown", "unavailable"]:
                try:
                    room_temp = float(state.state)
                    if "params" not in data: data["params"] = {}
                    if "cricuits" not in data["params"]: data["params"]["cricuits"] = [{}]
                    # Symulacja struktury dla parsera
                    data["params"]["cricuits"][0]["troomsetheat"] = room_temp * 10
                    data["params"]["cricuits"][0]["troomsetcool"] = room_temp * 10
                except ValueError:
                    pass
        
        return data

    def _has_valid_cookie(self):
        for cookie in self.session.cookie_jar:
            if cookie.key == "solaccess":
                return True
        return False

    async def _login(self):
        """Login to the service."""
        _LOGGER.debug("Próba logowania do HKS Lazar...")
        self.session.cookie_jar.clear() # Czyścimy stare ciastka przed nowym logowaniem
        
        payload = {"login": self.username, "password": self.password}
        async with self.session.post(LOGIN_URL, data=payload, timeout=10) as resp:
            resp.raise_for_status()
            
            found = False
            for cookie in self.session.cookie_jar:
                if cookie.key == "solaccess":
                    found = True
            if not found:
                raise ConfigEntryAuthFailed("Zalogowano, ale brak ciasteczka 'solaccess'.")
            _LOGGER.info("✅ Pomyślnie zalogowano/odświeżono sesję HKS Lazar")

    async def set_param(self, param, value):
        """Send command to set a parameter."""
        # Tutaj też dodajemy proste zabezpieczenie
        try:
            await self._send_param_request(param, value)
        except Exception:
            _LOGGER.warning("Błąd ustawiania parametru, ponawiam logowanie...")
            await self._login()
            await self._send_param_request(param, value)
        
        await self.async_request_refresh()

    async def _send_param_request(self, param, value):
        url = f"{SET_URL}&param={param}&value={value}"
        async with self.session.get(url, timeout=10) as resp:
            resp.raise_for_status()
        _LOGGER.info(f"SET {param} -> {value}")

    async def close(self):
        await self.session.close()

# Helper function moved inside to allow proper imports if needed, 
# though keeping it global is fine if other files import it.
def get_value_from_path(data, path):
    """Helper to traverse dot notation path."""
    try:
        keys = path.split(".")
        val = data
        for key in keys:
            if isinstance(val, list) and key.isdigit():
                val = val[int(key)]
            else:
                val = val[key]
        return val
    except (KeyError, TypeError, IndexError):
        return None
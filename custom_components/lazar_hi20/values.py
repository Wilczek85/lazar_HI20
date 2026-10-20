"""Pure value conversion helpers; no network or Home Assistant dependency."""
from math import isfinite


def numeric_value(raw, scale=1):
    """Decode finite API numbers; -9999 denotes a missing measurement."""
    if raw is None or isinstance(raw, bool):
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError, OverflowError):
        return None
    if not isfinite(value) or value == -9999:
        return None
    result = value * scale
    return result if isfinite(result) else None


def room_temperature(raw, unit):
    """Convert an HA room measurement to Celsius, refusing unknown units."""
    value = numeric_value(raw)
    if value is None:
        return None
    if unit == "°C":
        return value
    if unit == "°F":
        return (value - 32) * 5 / 9
    if unit == "K":
        return value - 273.15
    return None

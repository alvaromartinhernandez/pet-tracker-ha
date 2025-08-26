from .const import DOMAIN

async def async_setup_entry(hass, entry):
    """Set up Pet Event Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data.pop(DOMAIN, None)
    return True

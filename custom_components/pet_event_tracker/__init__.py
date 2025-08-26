from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Pet Event Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Servicio para registrar caca
    async def handle_log_poop(call: ServiceCall):
        hass.components.persistent_notification.create(
            "💩 ¡Se ha registrado una caca!",
            title="Pet Event Tracker"
        )
        # Aquí luego podemos guardar en storage o DB

    # Servicio para registrar pis
    async def handle_log_pee(call: ServiceCall):
        hass.components.persistent_notification.create(
            "💧 ¡Se ha registrado un pis!",
            title="Pet Event Tracker"
        )

    hass.services.async_register(DOMAIN, "log_poop", handle_log_poop)
    hass.services.async_register(DOMAIN, "log_pee", handle_log_pee)

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data.pop(DOMAIN, None)
    return True

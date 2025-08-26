# __init__.py
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN
from .storage import PetEventStorage

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Pet Event Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    storage = PetEventStorage(hass)
    hass.data[DOMAIN]["storage"] = storage

    # Servicio para registrar caca
    async def handle_log_poop(call: ServiceCall):
        storage.add_event("poop")
        hass.components.persistent_notification.create(
            "💩 ¡Se ha registrado una caca!",
            title="Pet Event Tracker"
        )
        # Actualizar entidades
        await update_sensors()

    # Servicio para registrar pis
    async def handle_log_pee(call: ServiceCall):
        storage.add_event("pee")
        hass.components.persistent_notification.create(
            "💧 ¡Se ha registrado un pis!",
            title="Pet Event Tracker"
        )
        # Actualizar entidades
        await update_sensors()

    async def update_sensors():
        """Actualizar todos los sensores registrados"""
        for entity in hass.data[DOMAIN].get("entities", []):
            entity.async_write_ha_state()

    hass.services.async_register(DOMAIN, "log_poop", handle_log_poop)
    hass.services.async_register(DOMAIN, "log_pee", handle_log_pee)

    # Setup sensors
    await hass.helpers.discovery.async_load_platform(
        "sensor", DOMAIN, {}, entry
    )

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data.pop(DOMAIN, None)
    return True
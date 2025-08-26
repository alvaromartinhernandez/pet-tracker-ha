import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class PetEventTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pet Event Tracker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Called when the user starts the setup from the UI."""
        if user_input is not None:
            # Aquí podrías guardar datos, pero de momento no hay opciones
            return self.async_create_entry(title="Pet Event Tracker", data={})

        # Si no hay datos, mostramos un formulario vacío
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )

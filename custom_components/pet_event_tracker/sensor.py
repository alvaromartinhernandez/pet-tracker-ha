from homeassistant.helpers.entity import Entity
from datetime import datetime, timedelta

DOMAIN = "pet_event_tracker"

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([PetTrackerSensor("pis"), PetTrackerSensor("caca")])

class PetTrackerSensor(Entity):
    def __init__(self, tipo):
        self._tipo = tipo
        self._state = None
        self._last_time = None

    @property
    def name(self):
        return f"Pet {self._tipo}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "last_time": self._last_time
        }

    def add_event(self):
        self._state = (self._state or 0) + 1
        self._last_time = datetime.now().isoformat()

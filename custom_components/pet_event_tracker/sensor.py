# sensor.py
from homeassistant.helpers.entity import Entity
from datetime import datetime, timedelta
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    storage = hass.data[DOMAIN]["storage"]
    
    sensors = [
        PetEventSensor(hass, "pee", "Pis"),
        PetEventSensor(hass, "poop", "Caca"),
        PetEventHistorySensor(hass, "history", "Historial")
    ]
    
    hass.data[DOMAIN]["entities"] = sensors
    async_add_entities(sensors, True)

class PetEventSensor(Entity):
    def __init__(self, hass, event_type, name):
        self._hass = hass
        self._event_type = event_type
        self._name = f"Pet {name}"
        self._state = 0
        self._last_time = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "last_time": self._last_time
        }

    def update(self):
        storage = self._hass.data[DOMAIN]["storage"]
        events = storage.get_recent_events(days=7)
        
        # Contar eventos de este tipo en los últimos 7 días
        self._state = sum(1 for event in events if event["type"] == self._event_type)
        
        # Encontrar el último evento
        last_event = next((event for event in events if event["type"] == self._event_type), None)
        self._last_time = last_event["timestamp"] if last_event else None

class PetEventHistorySensor(Entity):
    def __init__(self, hass, event_type, name):
        self._hass = hass
        self._event_type = event_type
        self._name = f"Pet {name}"
        self._state = 0
        self._events = []

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "events": self._events,
            "total_events": len(self._events)
        }

    def update(self):
        storage = self._hass.data[DOMAIN]["storage"]
        self._events = storage.get_recent_events(days=7)
        self._state = len(self._events)
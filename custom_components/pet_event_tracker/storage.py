# storage.py
import json
import os
from datetime import datetime, timedelta
from homeassistant.core import HomeAssistant

STORAGE_FILE = "pet_events.json"

class PetEventStorage:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self._data = {}
        self._load()

    def _get_storage_path(self):
        return os.path.join(self.hass.config.path(), STORAGE_FILE)

    def _load(self):
        try:
            with open(self._get_storage_path(), 'r') as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {"pee": [], "poop": []}

    def _save(self):
        with open(self._get_storage_path(), 'w') as f:
            json.dump(self._data, f)

    def add_event(self, event_type):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type
        }
        self._data[event_type].append(event)
        self._save()
        return event

    def get_recent_events(self, days=7):
        cutoff = datetime.now() - timedelta(days=days)
        all_events = []
        
        for event_type in ["pee", "poop"]:
            for event in self._data.get(event_type, []):
                event_time = datetime.fromisoformat(event["timestamp"])
                if event_time >= cutoff:
                    all_events.append({
                        "type": event_type,
                        "timestamp": event["timestamp"],
                        "time": event_time.strftime("%H:%M"),
                        "date": event_time.strftime("%Y-%m-%d")
                    })
        
        # Ordenar por fecha más reciente
        all_events.sort(key=lambda x: x["timestamp"], reverse=True)
        return all_events
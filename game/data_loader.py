import json
from pathlib import Path


def load_events():
    events = []

    events_directory = Path("data/events")

    for file_path in events_directory.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            file_events = json.load(file)

        events.extend(file_events)

    return events
import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("scores.json")


DEFAULT_DATA = {
    "theme": "Dark",
    "sound": True,
    "lifetime_scores": {
        "X": 0,
        "O": 0,
        "Draws": 0,
    },
}


def load_data():
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_DATA.copy()

    data.setdefault("theme", "Dark")
    data.setdefault("sound", True)
    data.setdefault("lifetime_scores", {"X": 0, "O": 0, "Draws": 0})
    return data


def save_data(data):
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError:
        pass

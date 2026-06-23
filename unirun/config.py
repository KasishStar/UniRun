import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "search_dirs": [
        "~/Downloads",
        "~/Documents",
        "~/Pictures",
        "~/Desktop",
        "~/Videos",
        "~/Music",
    ],
    "history_file": "~/.local/share/unirun/history.log",
    "wine_prefix": "~/.local/share/unirun/prefixes/default",
    "verbose": False,
}

class Config:
    def __init__(self, path):
        self._path = path
        self._data = {}
        self._load()

    def _load(self):
        path = os.path.expanduser(self._path)
        if os.path.exists(path):
            try:
                with open(path) as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._data = {}
        for key, val in DEFAULT_CONFIG.items():
            self._data.setdefault(key, val)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, val):
        self._data[key] = val
        self._save()

    def _save(self):
        path = os.path.expanduser(self._path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, 'w') as f:
                json.dump(self._data, f, indent=2)
        except OSError:
            pass

_config = None

def load_config():
    global _config
    if _config is None:
        path = os.environ.get("UNIRUN_CONFIG", "~/.config/unirun/config.json")
        _config = Config(path)
    return _config

def reset_config():
    global _config
    _config = None

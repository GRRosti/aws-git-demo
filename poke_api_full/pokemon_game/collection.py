import json
from pathlib import Path
from typing import Dict

try:
    from .config import JSON_FILE, logger, handle_error
except ImportError:
    from config import JSON_FILE, logger, handle_error

def initialize_json() -> None:
    """Initialize JSON file if it doesn't exist."""
    file_path = Path(JSON_FILE)
    if not file_path.exists():
        try:
            with file_path.open('w') as f:
                json.dump({"pokemon": []}, f, indent=2)
        except PermissionError:
            handle_error("Cannot create pokemon_collection.json. Check permissions.")

def load_pokemon_collection() -> Dict:
    """Load Pokémon collection from JSON."""
    try:
        with Path(JSON_FILE).open('r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"pokemon": []}

def save_pokemon_collection(data: Dict) -> None:
    """Save Pokémon collection to JSON."""
    try:
        with Path(JSON_FILE).open('w') as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        handle_error("Cannot write to pokemon_collection.json. Check permissions.")
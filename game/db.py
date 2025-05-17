import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
JSON_FILE = os.getenv("JSON_FILE", "pokemon_collection.json")

def initialize_json():
    """Initialize JSON file if it doesn't exist."""
    if not os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'w') as f:
                json.dump({"pokemon": []}, f, indent=2)
        except PermissionError:
            print("Error: Cannot create pokemon_collection.json. Check permissions.")
            sys.exit(1)

def load_pokemon_collection():
    """Load Pokémon collection from JSON."""
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"pokemon": []}

def save_pokemon_collection(data):
    """Save Pokémon collection to JSON."""
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        print("Error: Cannot write to pokemon_collection.json. Check permissions.")
        sys.exit(1)
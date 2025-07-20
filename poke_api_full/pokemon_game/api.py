import requests
from typing import List, Dict, Optional

try:
    from .config import POKEAPI_BASE, API_TIMEOUT, logger, handle_error
except ImportError:
    # Fallback for direct execution during debugging
    from config import POKEAPI_BASE, API_TIMEOUT, logger, handle_error

_pokemon_list_cache = None

def get_pokemon_list() -> List[str]:
    """Fetch or return cached Pokémon list from PokeAPI."""
    global _pokemon_list_cache
    if _pokemon_list_cache is None:
        try:
            response = requests.get(f"{POKEAPI_BASE}/pokemon?limit=1000", timeout=API_TIMEOUT)
            response.raise_for_status()
            _pokemon_list_cache = [p["name"] for p in response.json()["results"]]
        except requests.RequestException as e:
            logger.error(f"Error fetching Pokémon list: {e}")
            return []
    return _pokemon_list_cache

def get_pokemon_details(name: str) -> Optional[Dict]:
    """Fetch Pokémon details from PokeAPI."""
    try:
        response = requests.get(f"{POKEAPI_BASE}/pokemon/{name}", timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]],
            "height": data["height"]
        }
    except requests.RequestException as e:
        logger.error(f"Error fetching details for {name}: {e}")
        return None
from typing import Dict

try:
    from .config import logger
except ImportError:
    from config import logger

def display_pokemon(pokemon: Dict) -> None:
    """Display Pokémon details nicely."""
    logger.info("\n🎉 You drew a Pokémon! 🎉")
    logger.info(f"Name: {pokemon['name'].capitalize()}")
    logger.info(f"ID: {pokemon['id']}")
    logger.info(f"Types: {', '.join(pokemon['types'])}")
    logger.info(f"Height: {pokemon['height']} dm")
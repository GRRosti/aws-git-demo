import random
import sys
from typing import Dict

try:
    from .api import get_pokemon_list, get_pokemon_details
    from .collection import initialize_json, load_pokemon_collection, save_pokemon_collection
    from .display import display_pokemon
    from .config import logger
except ImportError:
    from api import get_pokemon_list, get_pokemon_details
    from collection import initialize_json, load_pokemon_collection, save_pokemon_collection
    from display import display_pokemon
    from config import logger

def run_game() -> None:
    """Main game loop."""
    initialize_json()
    logger.info("Welcome to Pokémon Draw! 🎮")
    
    while True:
        choice = input("\nWould you like to draw a Pokémon? (yes/no): ").lower().strip()
        
        if choice == "yes":
            pokemon_list = get_pokemon_list()
            if not pokemon_list:
                logger.error("Failed to fetch Pokémon list. Try again later.")
                continue
            
            random_pokemon = random.choice(pokemon_list)
            collection = load_pokemon_collection()
            existing_pokemon = next((p for p in collection["pokemon"] if p["name"] == random_pokemon), None)
            
            if existing_pokemon:
                logger.info(f"{random_pokemon.capitalize()} is already in your collection!")
                display_pokemon(existing_pokemon)
            else:
                pokemon_data = get_pokemon_details(random_pokemon)
                if pokemon_data:
                    collection["pokemon"].append(pokemon_data)
                    save_pokemon_collection(collection)
                    logger.info(f"Added {random_pokemon.capitalize()} to your collection!")
                    display_pokemon(pokemon_data)
                else:
                    logger.error(f"Could not add {random_pokemon}. Try again.")
        
        elif choice == "no":
            logger.info("\nThanks for playing! Gotta catch 'em all next time! 👋")
            break
        else:
            logger.warning("Please enter 'yes' or 'no'.")

def main() -> None:
    """Entry point."""
    try:
        run_game()
    except KeyboardInterrupt:
        logger.info("\nProgram terminated by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
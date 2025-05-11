import requests
import json
import random
import os
import sys
from pathlib import Path

# Constants
POKEAPI_BASE = "https://pokeapi.co/api/v2"
JSON_FILE = "pokemon_collection.json"

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

def get_pokemon_list():
    """Fetch list of Pokémon from PokeAPI."""
    try:
        response = requests.get(f"{POKEAPI_BASE}/pokemon?limit=1000")
        response.raise_for_status()
        return [p["name"] for p in response.json()["results"]]
    except requests.RequestException as e:
        print(f"Error fetching Pokémon list: {e}")
        return []

def get_pokemon_details(name):
    """Fetch Pokémon details from PokeAPI."""
    try:
        response = requests.get(f"{POKEAPI_BASE}/pokemon/{name}")
        response.raise_for_status()
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]],
            "height": data["height"]
        }
    except requests.RequestException as e:
        print(f"Error fetching details for {name}: {e}")
        return None

def display_pokemon(pokemon):
    """Display Pokémon details nicely."""
    print("\n🎉 You drew a Pokémon! 🎉")
    print(f"Name: {pokemon['name'].capitalize()}")
    print(f"ID: {pokemon['id']}")
    print(f"Types: {', '.join(pokemon['types'])}")
    print(f"Height: {pokemon['height']} dm")

def main():
    """Main program loop."""
    initialize_json()
    
    while True:
        choice = input("\nWould you like to draw a Pokémon? (yes/no): ").lower().strip()
        
        if choice == "yes":
            # Fetch Pokémon list
            pokemon_list = get_pokemon_list()
            if not pokemon_list:
                print("Failed to fetch Pokémon list. Try again later.")
                continue
            
            # Select random Pokémon
            random_pokemon = random.choice(pokemon_list)
            
            # Load collection
            collection = load_pokemon_collection()
            existing_pokemon = next((p for p in collection["pokemon"] if p["name"] == random_pokemon), None)
            
            if existing_pokemon:
                # Display existing Pokémon
                print(f"{random_pokemon.capitalize()} is already in your collection!")
                display_pokemon(existing_pokemon)
            else:
                # Fetch and save new Pokémon
                pokemon_data = get_pokemon_details(random_pokemon)
                if pokemon_data:
                    collection["pokemon"].append(pokemon_data)
                    save_pokemon_collection(collection)
                    print(f"Added {random_pokemon.capitalize()} to your collection!")
                    display_pokemon(pokemon_data)
                else:
                    print(f"Could not add {random_pokemon}. Try again.")
        
        elif choice == "no":
            print("\nThanks for playing! Gotta catch 'em all next time! 👋")
            break
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")
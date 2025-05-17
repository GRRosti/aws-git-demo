#!/bin/bash

# Ensure dependencies are installed
bash setup.sh || { echo "Failed to install dependencies"; exit 1; }

# Create executable
pyinstaller --onefile --name PokemonDraw pokemon_game/main.py || { echo "Failed to create executable"; exit 1; }

# Move executable to /usr/local/bin
sudo mv dist/PokemonDraw /usr/local/bin/ || { echo "Failed to move executable"; exit 1; }

# Clean up
rm -rf build dist *.spec

echo "Executable created and moved to /usr/local/bin/PokemonDraw"
echo "Run 'PokemonDraw' to play the game"
# backend-app/app.py
# Flask CRUD API for MongoDB

from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
# MONGO_URI will be set by docker-compose.yml
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/pokeapi_db')
client = MongoClient(MONGO_URI)
db = client.pokeapi_db
pokemon_collection = db.pokemon # Collection to store Pokemon data

@app.route('/')
def home():
    return "PokeAPI Backend is running!"

@app.route('/pokemon_game', methods=['POST'])
def create_pokemon():
    """Create a new Pokemon entry."""
    data = request.json
    if not data or 'name' not in data or 'type' not in data:
        return jsonify({"error": "Name and type are required"}), 400
    
    # Ensure unique names or handle duplicates as per game logic
    if pokemon_collection.find_one({'name': data['name']}):
        return jsonify({"error": "Pokemon with this name already exists"}), 409

    try:
        result = pokemon_collection.insert_one(data)
        data['_id'] = str(result.inserted_id) # Convert ObjectId to string for JSON
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pokemon', methods=['GET'])
def get_all_pokemon():
    """Retrieve all Pokemon entries."""
    try:
        pokemon_list = []
        for pokemon in pokemon_collection.find():
            pokemon['_id'] = str(pokemon['_id']) # Convert ObjectId to string
            pokemon_list.append(pokemon)
        return jsonify(pokemon_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pokemon/<id>', methods=['GET'])
def get_pokemon_by_id(id):
    """Retrieve a single Pokemon entry by ID."""
    try:
        pokemon = pokemon_collection.find_one({'_id': ObjectId(id)})
        if pokemon:
            pokemon['_id'] = str(pokemon['_id'])
            return jsonify(pokemon), 200
        return jsonify({"message": "Pokemon not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pokemon/<id>', methods=['PUT'])
def update_pokemon(id):
    """Update an existing Pokemon entry by ID."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    
    try:
        result = pokemon_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.matched_count > 0:
            return jsonify({"message": "Pokemon updated successfully"}), 200
        return jsonify({"message": "Pokemon not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pokemon/<id>', methods=['DELETE'])
def delete_pokemon(id):
    """Delete a Pokemon entry by ID."""
    try:
        result = pokemon_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Pokemon deleted successfully"}), 200
        return jsonify({"message": "Pokemon not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Flask runs on 0.0.0.0 to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000)

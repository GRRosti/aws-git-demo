import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
POKEAPI_BASE = "https://pokeapi.co/api/v2"
JSON_FILE = "pokemon_collection.json"
API_TIMEOUT = 5  # Seconds for API request timeout

def handle_error(message: str, exit_code: int = 1) -> None:
    """Log error and exit program."""
    logger.error(message)
    sys.exit(exit_code)
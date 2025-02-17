import importlib
import logging
import os

# Importer et charger les variables d'environnement depuis config.py
from config.config import load_env_variables, get_environment
from utils.utils_storage import ObjectStorageClient

load_env_variables()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

client = ObjectStorageClient()

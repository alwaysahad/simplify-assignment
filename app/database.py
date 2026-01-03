"""MongoDB database connection and configuration."""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "kuberi_gold")

# Lazy-loaded client to avoid connection errors at startup
_client = None
_db = None


def _get_client():
    """Get or create MongoDB client (lazy initialization)."""
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    return _client


def get_database():
    """Get database instance."""
    global _db
    if _db is None:
        _db = _get_client()[DATABASE_NAME]
    return _db


def get_purchases_collection():
    """Get purchases collection."""
    return get_database()["purchases"]


def get_chat_history_collection():
    """Get chat history collection."""
    return get_database()["chat_history"]

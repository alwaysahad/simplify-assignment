"""MongoDB database connection and configuration."""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "kuberi_gold")

# Create MongoDB client
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections
purchases_collection = db["purchases"]
chat_history_collection = db["chat_history"]


def get_database():
    """Get database instance."""
    return db


def get_purchases_collection():
    """Get purchases collection."""
    return purchases_collection


def get_chat_history_collection():
    """Get chat history collection."""
    return chat_history_collection

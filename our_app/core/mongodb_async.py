"""
MongoDB connection layer with async and sync clients.

Uses:
- motor: Async MongoDB driver
- pymongo: async client for lifespan

"""
from functools import lru_cache

from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from our_app.core.config import settings


_async_client: AsyncMongoClient | None = None

@lru_cache(maxsize=1)
def get_mongo_async_client() -> AsyncMongoClient:
    """
    Get async MongoDB database instance.

    Returns:
        Database: motor database object
    """

    global _async_client
    if _async_client is None:
        _async_client = AsyncMongoClient(
            str(settings.MONGODB_URI),
            server_api=ServerApi("1")
        )
    return _async_client

def close_mongo_async_client():
    """Close async MongoDB client."""
    global _async_client
    if _async_client is not None:
        _async_client.close()
        _async_client = None

def get_async_mongo_database():
    client = get_mongo_async_client()
    return client[settings.MONGODB_DB]

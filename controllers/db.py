from configs import Configs
from pymongo import MongoClient
from pymongo.collection import Collection as MongoCollection

client = MongoClient(Configs.DB_URL)
database = client[Configs.DB_DATABASE]


def get_collection(name: str) -> MongoCollection:
    """
    Get collection, create if not exists.
    """
    return database[name]

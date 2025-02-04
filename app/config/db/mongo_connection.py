from pymongo import MongoClient
from app.config.settings import Config

class MongoConnection:
    _client = None
    _db = None

    @staticmethod
    def get_db():
        if MongoConnection._client is None:
            MongoConnection._client = MongoClient(Config.MONGO_URI)
            MongoConnection._db = MongoConnection._client[Config.MONGO_DB_NAME]
        return MongoConnection._db

    @staticmethod
    def get_collection(name: str):
        db = MongoConnection.get_db()
        return db[name]
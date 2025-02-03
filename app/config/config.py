from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from pymongo import MongoClient
from flask_caching import Cache

from app.config.settings import Config

jwt = JWTManager()
redis_client = FlaskRedis()
mongo_client = MongoClient()
cache = Cache()

def init_extensions(app):
    jwt.init_app(app)
    redis_client.init_app(app)
    db_name = Config.MONGO_URI.rsplit("/", 1)[-1]
    app.mongo = mongo_client[db_name]
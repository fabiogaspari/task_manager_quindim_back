from pymongo import MongoClient
from flask_redis import FlaskRedis
from app.config.settings import Config

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client.get_database()

users_collection = db["user"]
tasks_collection = db["task"]
task_statuses_collection = db["task_status"]

redis_client = FlaskRedis()
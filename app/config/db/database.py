import time
from pymongo import MongoClient, errors
from app.config.settings import Config
from flask_redis import FlaskRedis
from flask_redis import FlaskRedis
from app.config.settings import Config

# Instancia o cliente Redis do Flask
redis_client = FlaskRedis()


def init_redis(app):
    redis_client.init_app(app, config_prefix='CACHE')

def wait_for_mongo():
    """ Aguarda o MongoDB estar disponível antes de continuar. """
    for _ in range(30):
        try:
            client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=3000)
            client.admin.command("ping")  # Testa conexão com o Mongo
            print("MongoDB está pronto!")
            return client
        except errors.ServerSelectionTimeoutError:
            print("Aguardando o MongoDB iniciar...")
            time.sleep(2)
    raise Exception("MongoDB não está acessível!")

def init_dbs():
    mongo_client = wait_for_mongo()
    db = mongo_client[Config.MONGO_DB_NAME]
    collections = ["user", "task", "task_status"]

    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
            print(f"Collection '{collection}' criada com sucesso.")
        else:
            print(f"Collection '{collection}' já existe.")

    mongo_client.close()

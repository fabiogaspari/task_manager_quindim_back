from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging

from app.config.settings import Config
from app.config.db.database import init_dbs, init_redis
from app.config.config import init_extensions, cache
from app.config.cache import cache

def create_app():
    app = Flask(__name__)

    CORS(app, origins="http://localhost:5173")
    app.config.from_object(Config)

    JWTManager(app)

    cache.init_app(app)
    init_dbs()
    init_redis(app)
    init_extensions(app)

    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://redis:6379/0'  # Corrigido para usar o nome do serviço Redis no Docker

    from app.api.controller.auth import auth_bp
    from app.api.controller.task import task_auth_bp
    from app.api.controller.task_status import task_status_auth_bp
    from app.api.controller.user import auth_user_bp

    app.register_blueprint(auth_bp, url_prefix="/auth/users")
    app.register_blueprint(task_auth_bp, url_prefix="/tasks")
    app.register_blueprint(task_status_auth_bp, url_prefix="/task_statuses")
    app.register_blueprint(auth_user_bp, url_prefix="/users")

    logging.basicConfig(
        filename='backend_errors.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    return app
from flask import Flask
from flask_jwt_extended import JWTManager
from app.config.settings import Config
from app.config.db.database import redis_client
from app.config.config import init_extensions
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app, origins="http://localhost:5173")
    app.config.from_object(Config)

    JWTManager(app)
    redis_client.init_app(app)

    init_extensions(app)

    from app.api.controller.auth import auth_bp
    from app.api.controller.task import task_auth_bp
    from app.api.controller.task_status import task_status_auth_bp
    from app.api.controller.user import auth_user_bp

    app.register_blueprint(auth_bp, url_prefix="/auth/users")
    app.register_blueprint(task_auth_bp, url_prefix="/tasks")
    app.register_blueprint(task_status_auth_bp, url_prefix="/task_statuses")
    app.register_blueprint(auth_user_bp, url_prefix="/users")

    return app
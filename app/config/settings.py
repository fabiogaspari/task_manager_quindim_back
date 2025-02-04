class Config:
    SECRET_KEY = "VF6mEue18tP4DohYWk4wTjrL9hY7"
    JWT_SECRET_KEY = "KY0c9Kzm1W6HF3iK5lWDV4M7V4FO"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    REDIS_URL = "redis://redis:6379/0"  # Corrigido para usar o nome do serviço Redis no Docker
    MONGO_URI = "mongodb://mongo:27017/task_manager"  # Corrigido para usar o nome do serviço Mongo no Docker
    MONGO_DB_NAME = "task_manager"
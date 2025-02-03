from flask import request
from flask_jwt_extended import create_access_token, get_jwt

from app.config.db.database import redis_client
from app.config.db.database import users_collection
from app.api.service.user_service import UserService
from app.util.auth.auth_util import verify_password
from app.util.format.serialize_util import objectid_to_str
from app.api.model.response.user_response import UserResponse
from app.api.model.user_model import UserModel


class AuthService:
    @staticmethod
    def register() ->  str:
        token = UserService.create()
        return token
    
    @staticmethod
    def verify_token() ->  str:
        token = UserService.create()
        return token
    
    @staticmethod
    def login() -> dict:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user: UserModel = users_collection.find_one({"email": email})
        
        # verifica se a senha esta correta, para o usuário requisitado
        if not user or not verify_password(user["password"], password):
            raise PermissionError("Usuário ou senha incorretos.")

        # armazena o id do usuário no redis e retorna o token
        token = create_access_token(identity=str(user["email"]))

        return {"token": token, "user": UserResponse(objectid_to_str(user["_id"]), user["username"], user["email"]).to_dict()}

    @staticmethod
    def logout() -> bool:
        jwt = get_jwt()
        jti = jwt["jti"]

        if not jti:
            raise PermissionError("O usuário não tem permissão para realizar essa ação.")
        
        try:
            deleted = redis_client.delete(jti)
            return deleted > 0
        except ConnectionError as e:
            return False
    
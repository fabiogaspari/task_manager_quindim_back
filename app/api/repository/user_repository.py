from flask_jwt_extended import get_jwt_identity
from pymongo.errors import PyMongoError
from typing import List

from app.api.model.user_model import UserModel
from app.api.model.response.user_response import UserResponse
from app.config.db.mongo_connection import MongoConnection
from app.util.format.serialize_util import objectid_to_str
from app.api.repository.contract.user_interface_repository import UserInterfaceRepository
from app.util.repository.repository_util import RepositoryUtil

class UserRepository(UserInterfaceRepository):
    @staticmethod
    def create(user: UserModel) -> str:
        result = MongoConnection.get_collection('user').insert_one(user)
        if not result:
            raise PyMongoError("Erro ao criar o usuário no banco de dados.")
        return str(result.inserted_id)
        
    @staticmethod
    def get_all() -> List[UserModel]:
        user_email = get_jwt_identity()

        field_dict = {
            "email": user_email
        }
        users: UserModel = MongoConnection.get_collection('user').find(field_dict)
        user_list = list(users)
        
        for user in user_list:
            user["_id"] = objectid_to_str(user["_id"])

        return user_list
    
    @staticmethod
    def get_by_username(username) -> UserModel:
        user_email = get_jwt_identity()

        field_dict = {
            "username": username,
            "email": user_email
        }
        user: UserModel = RepositoryUtil.find_or_fail(MongoConnection.get_collection('user'), field_dict)
        user["_id"] = objectid_to_str(user["_id"])
        
        return UserResponse(objectid_to_str(user["_id"]), user["username"], user["email"]).to_dict()
    
    @staticmethod
    def get_by_email(email) -> UserModel:
        user_email = get_jwt_identity()
        
        if user_email is email:
            field_dict = {
                "email": user_email
            }
            user: UserModel = RepositoryUtil.find_or_fail(MongoConnection.get_collection('user'), field_dict)
        else:
            raise PermissionError("Usuário ou senha incorretos.")
        
        return UserResponse(objectid_to_str(user["_id"]), user["username"], user["email"]).to_dict()

    @staticmethod
    def update(update_data) -> bool:
        user_email = get_jwt_identity()

        RepositoryUtil.allowed_by_user(MongoConnection.get_collection('user'))

        result = MongoConnection.get_collection('user').update_one(
            {"email": user_email},
            {"$set": update_data}
        )

        return RepositoryUtil.modified(result)

    @staticmethod
    def delete() -> bool:
        RepositoryUtil.allowed_by_user(MongoConnection.get_collection('user'))

        field_data = {
            "is_deactivated": True
        }
        return UserRepository.update(field_data)
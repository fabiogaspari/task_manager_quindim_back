from flask_jwt_extended import get_jwt_identity
from bson.objectid import ObjectId
from pydantic import BaseModel

from app.api.exception.object_not_modified import ObjectNotModified
from app.config.db.mongo_connection import MongoConnection
from app.api.model.user_model import UserModel

class RepositoryUtil:
    @staticmethod
    def exist(obj) -> None:
        if not obj:
            raise AttributeError("Objeto não encontrado.")
        
    @staticmethod
    def find_or_fail(collection, field_dict) -> BaseModel:
        obj = collection.find_one(field_dict)
        
        RepositoryUtil.exist(obj)
        
        return obj
    
    @staticmethod
    def allowed_by_id(collection,  obj_id) -> BaseModel:
        user_email = get_jwt_identity()
        
        field_dict = {
            "_id": ObjectId(obj_id),
            "user.email": user_email
        }
        obj = collection.find_one(field_dict)
        RepositoryUtil.exist(obj)

        return obj
    
    def allowed_by_user(collection) -> UserModel:
        user_email = get_jwt_identity()

        user: UserModel = MongoConnection.get_collection('user').find_one({"email": user_email})
        RepositoryUtil.exist(user)

        return user
        

    @staticmethod
    def modified(result) -> bool:
        if result.modified_count > 0:
            return True
        else:
            raise ObjectNotModified
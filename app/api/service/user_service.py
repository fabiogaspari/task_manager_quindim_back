from flask import request
from typing import List
from datetime import datetime

from app.api.repository.user_repository import UserRepository
from app.api.model.user_model import UserModel
from app.util.auth.auth_util import hash_password

class UserService:
    @staticmethod
    def create():   
        data = request.get_json()
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        hashed_password = hash_password(password)
        user = UserModel(
            username=username,
            email=email,
            password=hashed_password,
            is_deactivated=False
        )

        user = user.model_dump()
        user_id = UserRepository.create(user)
        return user_id

    @staticmethod
    def get_all() -> List[UserModel]:
        return UserRepository.get_all()

    @staticmethod
    def get_by_id() -> UserModel:
        return UserRepository.get_by_id()
        
    @staticmethod
    def get_by_username(username) -> UserModel:
        user = UserRepository.get_by_username(username)
        return user
    
    @staticmethod
    def get_by_email(email) -> UserModel:
        user = UserRepository.get_by_email(email)
        return user
    
    @staticmethod
    def update() -> bool:
        data = request.get_json()

        update_data = {}

        username = data.get("username")
        if username:
            update_data["username"] = username
        
        password = data.get("password")
        if password:
            hashed_password = hash_password(password)
            update_data["password"] = hashed_password
        
        email = data.get("email")
        if email:
            update_data["email"] = email

        return UserRepository.update(update_data)
    
    @staticmethod
    def delete() -> bool:
        return UserRepository.delete()
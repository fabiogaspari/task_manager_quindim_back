from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from typing import List

from app.api.repository.task_status_repository import TaskStatusRepository
from app.api.model.task_status_model import TaskStatusModel
from app.api.model.user_model import UserModel
from app.api.service.user_service import UserService
from app.api.service.contract.interface_service import InterfaceService

class TaskStatusService(InterfaceService):
    @staticmethod
    def create() -> str:
        data = request.get_json()
        user_email = get_jwt_identity()

        user: UserModel = UserService.get_by_email(user_email)
        
        name = data.get("name")
        status_color = data.get("status_color")
        status_color_font = data.get("status_color_font")
        description = data.get("description")
        
        task_status = TaskStatusModel(
            name=name,
            status_color=status_color,
            status_color_font=status_color_font,
            description=description,
            user=user
        )

        task_status_id = TaskStatusRepository.create(task_status)
        return str(task_status_id)
    
    @staticmethod
    def get_all() -> List[TaskStatusModel]:
        return TaskStatusRepository.get_all()
    
    @staticmethod
    def get_by_id(task_status_id) -> TaskStatusModel:
        return TaskStatusRepository.get_by_id(task_status_id)
        
    @staticmethod
    def update(task_status_id) -> jsonify:
        data = request.get_json()

        update_data = {}
        name = data.get("name")
        if name:
            update_data["name"] = name
        
        status_color = data.get("status_color")
        if status_color:
            update_data["status_color"] = status_color
        
        status_color_font = data.get("status_color_font")
        if status_color_font:
            update_data["status_color_font"] = status_color_font

        description = data.get("description")
        if description:
            update_data["description"] = description

        return TaskStatusRepository.update(task_status_id, update_data)
    
    @staticmethod
    def delete(task_status_id) -> jsonify:
        return TaskStatusRepository.delete(task_status_id)
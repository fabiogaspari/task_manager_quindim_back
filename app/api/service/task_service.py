from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from typing import List
from bson import ObjectId
from datetime import datetime

from app.api.repository.task_repository import TaskRepository
from app.api.model.task_model import TaskModel
from app.api.model.user_model import UserModel
from app.api.service.user_service import UserService
from app.api.repository.task_status_repository import TaskStatusRepository
from app.api.model.task_status_model import TaskStatusModel
from app.api.exception.task_status_on_task_not_found import TaskStatusOnTaskNotFound
from app.api.service.contract.interface_service import InterfaceService
from app.util.format.serialize_util import objectid_to_str

class TaskService(InterfaceService):
    @staticmethod
    def create() -> str:
        data = request.get_json()
        user_email = get_jwt_identity()
        status = data.get("status")
        
        user: UserModel = UserService.get_by_email(user_email)
        
        if "_id" in status:
            task_status_id = status["_id"]
            try:
                task_status = TaskStatusRepository.get_by_id(ObjectId(task_status_id))
                print(task_status)
            except AttributeError:
                raise TaskStatusOnTaskNotFound
        else:
            try:
                existing_task_status = TaskStatusRepository.get_by_name(status["name"])
                task_status = existing_task_status
                task_status_id = task_status["_id"]
            except AttributeError:
                task_status = TaskStatusModel(
                    name=status["name"],
                    status_color=status["status_color"],
                    status_color_font=status["status_color_font"],
                    description=status["description"],
                    user=user
                )
                task_status_id = TaskStatusRepository.create(task_status)
        title = data.get("title")
        expiration_date = data.get("expiration_date")
        try: 
            task_status["_id"] = objectid_to_str(task_status["_id"])
        except:
            pass

        task = TaskModel(
            title=title,
            status=task_status,
            expiration_date=expiration_date,
            user=user
        )
        task_id = TaskRepository.create(task)

        return task_id
    
    @staticmethod
    def get_all() -> List[TaskModel]:
        return TaskRepository.get_all()
    
    @staticmethod
    def get_by_id(task_id) -> TaskModel:
        return TaskRepository.get_by_id(task_id)
    
    @staticmethod
    def update(task_id) -> bool:
        data = request.get_json()

        update_data = {}
        title = data.get("title")
        if title:
            update_data["title"] = title
        
        expiration_date = data.get("expiration_date")
        if expiration_date:
            update_data["expiration_date"] = datetime.strptime(expiration_date, '%Y-%m-%d') 
        
        status = data.get("status")
        if status:
            update_data["status"] = status
        
        return TaskRepository.update(task_id, update_data)
    
    @staticmethod
    def delete(task_id) -> jsonify:
        return TaskRepository.delete(task_id)

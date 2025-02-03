from flask_jwt_extended import get_jwt_identity
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from typing import List

from app.config.db.database import tasks_collection
from app.util.format.serialize_util import objectid_to_str
from app.api.model.task_model import TaskModel
from app.api.repository.contract.default_interface_repository import DefaultInterfaceRepository
from app.util.repository.repository_util import RepositoryUtil

class TaskRepository(DefaultInterfaceRepository):
    @staticmethod
    def create(task: TaskModel) -> str:
        result = tasks_collection.insert_one(task.to_dict())
        if not result:
            raise PyMongoError("Erro ao criar a tarefa no banco de dados.")
        return str(result.inserted_id)
    
    @staticmethod
    def get_all() -> List[TaskModel]:
        user_email = get_jwt_identity()
        
        field_dict = {
            "user.email": user_email
        }
        tasks = tasks_collection.find(field_dict)
        task_list = list(tasks)

        for task in task_list:
            task["_id"] = objectid_to_str(task["_id"])
        
        return task_list

    @staticmethod
    def get_by_id(task_id) -> TaskModel:
        user_email = get_jwt_identity()
        
        field_dict = {
            "_id": ObjectId(task_id),
            "user.email": user_email
        }
        task = RepositoryUtil.find_or_fail(tasks_collection, field_dict)
        task["_id"] = task_id

        return task

    @staticmethod
    def get_by_title(title) -> TaskModel:
        user_email = get_jwt_identity()

        field_dict = {
            "title": title,
            "user.email": user_email
        }
        task = RepositoryUtil.find_or_fail(tasks_collection, field_dict)
        
        return task

    @staticmethod
    def update(task_id, update_data) -> bool:
        user_email = get_jwt_identity()

        RepositoryUtil.allowed_by_id(tasks_collection, task_id)
        result = tasks_collection.update_one(
            {"user.email": user_email, "_id": ObjectId(task_id)},
            {"$set": update_data}
        )

        return RepositoryUtil.modified(result)

    @staticmethod
    def delete(task_id) -> bool:
        user_email = get_jwt_identity()

        RepositoryUtil.allowed_by_id(tasks_collection, task_id)

        field_data = {
            "_id": ObjectId(task_id),
            "user.email": user_email
        }
        return tasks_collection.delete_one(field_data)
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from typing import List
from pymongo.errors import PyMongoError

from app.config.db.database import tasks_collection
from app.config.db.database import task_statuses_collection
from app.api.model.task_status_model import TaskStatusModel
from app.util.format.serialize_util import objectid_to_str
from app.api.repository.contract.default_interface_repository import DefaultInterfaceRepository
from app.util.repository.repository_util import RepositoryUtil
from app.config.cache import cache

class TaskStatusRepository(DefaultInterfaceRepository):
    @staticmethod
    def create(task_status: TaskStatusModel) -> str:
        result = task_statuses_collection.insert_one(task_status.to_dict())
        if not result:
            raise PyMongoError("Erro ao criar o status da tarefa no banco de dados.")
        return str(result.inserted_id)
    
    @staticmethod
    def get_all() -> List[TaskStatusModel]:
        user_email = get_jwt_identity()

        field_dict = {
            "user.email": user_email
        }
        task_statuses = task_statuses_collection.find(field_dict)
        task_status_list = list(task_statuses)
        
        for task_status in task_status_list:
            task_status["_id"] = objectid_to_str(task_status["_id"])

        return task_status_list

    @staticmethod
    def get_by_id(task_status_id) -> TaskStatusModel:
        user_email = get_jwt_identity()

        field_dict = {
            "_id": ObjectId(task_status_id),
            "user.email": user_email
        }
        task_status = RepositoryUtil.find_or_fail(task_statuses_collection, field_dict)
        task_status["_id"] = task_status_id

        return task_status

    @staticmethod
    def get_by_name(name) -> TaskStatusModel:
        user_email = get_jwt_identity()
        
        field_dict = {
            "name": name,
            "user.email": user_email
        }
        task_status = RepositoryUtil.find_or_fail(task_statuses_collection, field_dict)
        task_status["_id"] = objectid_to_str(task_status["_id"])
        return task_status

    @staticmethod
    def update(task_status_id, update_data) -> bool:
        user_email = get_jwt_identity()

        obj = RepositoryUtil.allowed_by_id(task_statuses_collection, task_status_id)
        search_dict = {}

        result = task_statuses_collection.update_one(
            {"user.email": user_email, "_id": ObjectId(task_status_id)},
            {"$set": update_data}
        )

        search_dict["status.name"] = obj["name"]
        search_dict["status.status_color"] = obj["status_color"]
        search_dict["status.status_color_font"] = obj["status_color_font"]
        search_dict["status.description"] = obj["description"]
        task_status = task_statuses_collection.find_one({"_id": ObjectId(task_status_id)})
        task_status["_id"] = objectid_to_str(task_status["_id"])
        tasks = tasks_collection.find(search_dict)
        for task in tasks:
            task["status"] = task_status
            tasks_collection.update_many(search_dict, {"$set": task})
        
        return RepositoryUtil.modified(result)

    @staticmethod
    def delete(task_status_id) -> bool:
        task_status_id = ObjectId(task_status_id)
        user_email = get_jwt_identity()

        RepositoryUtil.allowed_by_id(task_statuses_collection, task_status_id)

        field_data = {
            "_id": ObjectId(task_status_id),
            "user.email": user_email
        }
        return task_statuses_collection.delete_one(field_data)
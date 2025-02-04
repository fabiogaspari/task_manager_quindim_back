from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from typing import List
from pymongo.errors import PyMongoError

from app.config.db.mongo_connection import MongoConnection
from app.api.model.task_status_model import TaskStatusModel
from app.util.format.serialize_util import objectid_to_str
from app.api.repository.contract.default_interface_repository import DefaultInterfaceRepository
from app.util.repository.repository_util import RepositoryUtil
from app.config.cache import cache

class TaskStatusRepository(DefaultInterfaceRepository):
    @staticmethod
    def create(task_status: TaskStatusModel) -> str:
        result = MongoConnection.get_collection('task_status').insert_one(task_status.to_dict())
        if not result:
            raise PyMongoError("Erro ao criar o status da tarefa no banco de dados.")
        return str(result.inserted_id)
    
    @staticmethod
    def get_all() -> List[TaskStatusModel]:
        user_email = get_jwt_identity()

        field_dict = {
            "user.email": user_email
        }
        task_statuses = MongoConnection.get_collection('task_status').find(field_dict)
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
        task_status = RepositoryUtil.find_or_fail(MongoConnection.get_collection('task_status'), field_dict)
        task_status["_id"] = task_status_id

        return task_status

    @staticmethod
    def get_by_name(name) -> TaskStatusModel:
        user_email = get_jwt_identity()
        
        field_dict = {
            "name": name,
            "user.email": user_email
        }
        task_status = RepositoryUtil.find_or_fail(MongoConnection.get_collection('task_status'), field_dict)
        task_status["_id"] = objectid_to_str(task_status["_id"])
        return task_status

    @staticmethod
    def update(task_status_id, update_data) -> bool:
        user_email = get_jwt_identity()

        old_task_status = RepositoryUtil.allowed_by_id(MongoConnection.get_collection('task_status'), task_status_id)

        result = MongoConnection.get_collection('task_status').update_one(
            {"user.email": user_email, "_id": ObjectId(task_status_id)},
            {"$set": update_data}
        )
        task_status = MongoConnection.get_collection('task_status').find_one({"_id": ObjectId(task_status_id)})
        
        search_dict = {}
        search_dict["status.name"] = old_task_status["name"]
        search_dict["status.status_color"] = old_task_status["status_color"]
        search_dict["status.status_color_font"] = old_task_status["status_color_font"]
        search_dict["status.description"] = old_task_status["description"]
        tasks = MongoConnection.get_collection('task_status').find(search_dict)
        updated = RepositoryUtil.modified(result)

        task_list = list(tasks)
        
        if updated:
            for task in task_list:
                try:
                    task_status["_id"] = objectid_to_str(task_status["_id"])
                except:
                    task_status["_id"] = task_status["_id"]
                task_id = task["_id"]
                task.pop("_id")
                task["status"] = task_status
                MongoConnection.get_collection('task_status').update_one(
                    {"_id": task_id}, {"$set": task}
                )
        
        print(1)
        return updated

    @staticmethod
    def delete(task_status_id) -> bool:
        task_status_id = ObjectId(task_status_id)
        user_email = get_jwt_identity()

        RepositoryUtil.allowed_by_id(MongoConnection.get_collection('task_status'), task_status_id)

        field_data = {
            "_id": ObjectId(task_status_id),
            "user.email": user_email
        }
        return MongoConnection.get_collection('task_status').delete_one(field_data)
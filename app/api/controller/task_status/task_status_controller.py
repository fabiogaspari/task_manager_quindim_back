from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from app.api.service.task_status_service import TaskStatusService
from app.api.exception.object_not_modified import ObjectNotModified
from app.util.controller.controller_util import ControllerUtil
from app.config.cache import cache

from . import task_status_auth_bp

@task_status_auth_bp.route("/create", methods=["POST"])
@jwt_required()
def create() -> jsonify:
    try:
        task_status_id = TaskStatusService.create()
        cache.delete(f"task_get_all{get_jwt_identity()}")
        cache.delete(f"task_get{get_jwt_identity()}")
        cache.delete(f"task_status_get_all{get_jwt_identity()}")
        cache.delete(f"task_status_get{get_jwt_identity()}")
        return jsonify({"msg": "Status da tarefa criado com sucesso", "id": task_status_id}), 201
    except ValueError as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except Exception as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
    
@task_status_auth_bp.route("/all", methods=["GET"])
@jwt_required()
@cache.cached(key_prefix=lambda: f"task_status_get_all{get_jwt_identity()}")
def get_all() -> jsonify:
    try:
        task_statuses = TaskStatusService.get_all()
        return jsonify(task_statuses), 200
    except AttributeError as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Os status da tarefa não foram encontrada."}), 400
    except Exception as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@cache.cached(key_prefix=lambda: f"task_status_get{get_jwt_identity()}")  
@task_status_auth_bp.route("/<task_status_id>", methods=["GET"])
@jwt_required()
def get(task_status_id) -> jsonify:
    try:
        task_status = TaskStatusService.get_by_id(task_status_id)
        return jsonify(task_status), 200
    except AttributeError as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "O status da tarefa não foi encontrada."}), 400
    except Exception as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_status_auth_bp.route("/<task_status_id>", methods=["PUT"])
@jwt_required()
def update(task_status_id) -> jsonify:
    try:
        TaskStatusService.update(task_status_id)
        cache.delete(f"task_get_all{get_jwt_identity()}")
        cache.delete(f"task_get{get_jwt_identity()}")
        cache.delete(f"task_status_get_all{get_jwt_identity()}")
        cache.delete(f"task_status_get{get_jwt_identity()}")
        return jsonify({"msg": "O status da tarefa foi modificada com sucesso."}), 200
    except ValueError as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except AttributeError as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "O status da tarefa não foi encontrada."}), 400
    except ObjectNotModified as e:
        return jsonify({"msg": str(e)}), 200
    except Exception as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_status_auth_bp.route("/<task_status_id>", methods=["DELETE"])
@jwt_required()
def delete(task_status_id) -> jsonify:
    try:
        if TaskStatusService.delete(task_status_id):
            cache.delete(f"task_get_all{get_jwt_identity()}")
            cache.delete(f"task_get{get_jwt_identity()}")
            cache.delete(f"task_status_get_all{get_jwt_identity()}")
            cache.delete(f"task_status_get{get_jwt_identity()}")
            return jsonify({"msg": "Sucesso ao excluir o registro."}), 200
    except AttributeError as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "O status da tarefa não foi encontrada."}), 400
    except Exception as e:
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.api.service.task_status_service import TaskStatusService
from app.api.exception.object_not_modified import ObjectNotModified
from app.util.controller.controller_util import ControllerUtil

from . import task_status_auth_bp

@task_status_auth_bp.route("/create", methods=["POST"])
@jwt_required()
def create() -> jsonify:
    try:
        task_status_id = TaskStatusService.create()
        return jsonify({"msg": "Status da tarefa criado com sucesso", "task_status_id": task_status_id}), 201
    except ValueError as e:
        print(e)
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
    
@task_status_auth_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all() -> jsonify:
    try:
        task_statuses = TaskStatusService.get_all()
        return jsonify(task_statuses), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "Os status da tarefa não foram encontrada."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
    
@task_status_auth_bp.route("/<task_status_id>", methods=["GET"])
@jwt_required()
def get(task_status_id) -> jsonify:
    try:
        task_status = TaskStatusService.get_by_id(task_status_id)
        return jsonify(task_status), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "O status da tarefa não foi encontrada."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_status_auth_bp.route("/<task_status_id>", methods=["PUT"])
@jwt_required()
def update(task_status_id) -> jsonify:
    try:
        task_status = TaskStatusService.update(task_status_id)
        return jsonify({"msg": "O status da tarefa foi modificada com sucesso.", "task": task}), 200
    except ValueError as e:
        print(e)
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "O status da tarefa não foi encontrada."}), 400
    except ObjectNotModified as e:
        return jsonify({"msg": str(e)}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_status_auth_bp.route("/<task_status_id>", methods=["DELETE"])
@jwt_required()
def delete(task_status_id) -> jsonify:
    try:
        if TaskStatusService.delete(task_status_id):
            return jsonify({"msg": "Sucesso ao excluir o registro."}), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "O status da tarefa não foi encontrada."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
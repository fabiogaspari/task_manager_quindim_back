from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.service.task_service import TaskService
from app.api.exception.task_status_on_task_not_found import TaskStatusOnTaskNotFound
from app.api.exception.object_not_modified import ObjectNotModified
from app.util.controller.controller_util import ControllerUtil
from app.config.cache import cache

from . import task_auth_bp

@task_auth_bp.route("/create", methods=["POST"])
@jwt_required()
def create() -> jsonify:
    try:
        task_id = TaskService.create()
        return jsonify({"msg": "Tarefa criada com sucesso", "id": str(task_id)}), 201
    except ValueError as e:
        print(e)
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except TaskStatusOnTaskNotFound as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_auth_bp.route("/all", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60, key_prefix=lambda: f"task_{get_jwt_identity()}")
def get_all() -> jsonify:
    try:
        tasks = TaskService.get_all()
        return jsonify(tasks), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "As tarefas não foram encontradas."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_auth_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get(task_id) -> jsonify:
    try:
        task = TaskService.get_by_id(task_id)
        return jsonify(task), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "A tarefa não foi encontrada."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_auth_bp.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update(task_id) -> jsonify:
    try:
        TaskService.update(task_id)
        return jsonify({"msg": "A tarefa foi modificada com sucesso."}), 200
    except ValueError as e:
        print(e)
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "A tarefa não foi encontrada."}), 400
    except ObjectNotModified as e:
        return jsonify({"msg": str(e)}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@task_auth_bp.route("/<task_id>", methods=["DELETE"])
@jwt_required()
def delete(task_id) -> jsonify:
    try:
        TaskService.delete(task_id)
        return jsonify({"msg": "Tarefa excluida com sucesso."}), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "A tarefa não foi encontrada."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
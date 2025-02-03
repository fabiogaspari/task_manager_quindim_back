from flask import jsonify
from flask_jwt_extended import jwt_required
from pymongo.errors import PyMongoError

from app.api.service.auth.auth_service import AuthService
from app.api.service.user_service import UserService
from app.api.exception.object_not_modified import ObjectNotModified
from app.util.controller.controller_util import ControllerUtil

from . import auth_user_bp

@auth_user_bp.route("/create", methods=["POST"])
def create():
    try:
        user_id = AuthService.register()
        return jsonify({"msg": "Usuário criado com sucesso", "user_id": user_id}), 201
    except PyMongoError as e:
        print(e)
        return jsonify({"msg": str(2)}), 400
    except ValueError as e:
        print(e)
        return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
    
@auth_user_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all() -> jsonify:
    try:
        users = UserService.get_all()
        return jsonify(users), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "Os usuários não foram encontrados."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@auth_user_bp.route("/", methods=["GET"])
@jwt_required()
def get():
    try:
        task = UserService.get_by_id()
        return jsonify(task), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "O usuário não foi encontrado."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

# @auth_user_bp.route("/", methods=["PUT"])
# @jwt_required()
# def update():
#     try:
#         UserService.update()
#         return jsonify({"msg": "O usuário foi modificada com sucesso."}), 200
#     except ValueError as e:
#         print(e)
#         return jsonify({"errors": ControllerUtil.treat_value_error(e)}), 400
#     except AttributeError as e:
#         print(e)
#         return jsonify({"msg": "O usuário não foi encontrado."}), 400
#     except ObjectNotModified as e:
#         return jsonify({"msg": str(e)}), 200
#     except Exception as e:
#         print(e)
#         return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500

@auth_user_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete():
    try:
        if UserService.delete():
            return jsonify({"msg": "Sucesso ao excluir o registro."}), 200
    except AttributeError as e:
        print(e)
        return jsonify({"msg": "O usuário não foi encontrado."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500
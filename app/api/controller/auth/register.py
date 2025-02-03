from flask import jsonify
from pymongo.errors import PyMongoError

from app.api.service.auth.auth_service import AuthService

from . import auth_bp

@auth_bp.route("/register", methods=["POST"])
def register() ->  jsonify:
    try:
        user_id = AuthService.register()
        return jsonify({"msg": "Objeto criado com sucesso.", "_id": user_id}), 201
    except PyMongoError as e:
        return jsonify({"msg": {str(e)}}), 400
    except ValueError as e:
        error_message = str(e).split(",")[1].strip().split("[")[0].strip()
        return jsonify({"msg": error_message}), 400
    except Exception as e:
        print(str(e))
        return jsonify({"msg": "Ocorreu um erro inesperado. Por favor, tente mais tarde."}), 500


    
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.api.service.auth.auth_service import AuthService

from . import auth_bp

@auth_bp.route("/login", methods=["POST"])
def login() -> jsonify:
    try:
        response = AuthService.login()
        return jsonify(response), 200
    except PermissionError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Erro ao realizar o login. Por favor, verifique as informações ou tente mais tarde."}), 400

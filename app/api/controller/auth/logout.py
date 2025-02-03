from flask import jsonify
from flask_jwt_extended import jwt_required
from redis.exceptions import ConnectionError

from app.api.service.auth.auth_service import AuthService

from . import auth_bp

@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout() -> jsonify:
    try:
        logout = AuthService.logout()
        print(logout)
        return jsonify({"msg": "Logout realizado com sucesso."}), 200
    except PermissionError as e:
        return jsonify({"msg": str(e)}), 401
    except ConnectionError as e:
        return jsonify({"msg": str(e)}), 500
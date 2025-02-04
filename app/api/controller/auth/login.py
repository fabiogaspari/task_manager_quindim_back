from flask import jsonify
import logging

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
        logging.error(f"Erro no sistema: {e}")
        return jsonify({"msg": "Erro ao realizar o login. Por favor, verifique as informações ou tente mais tarde."}), 400

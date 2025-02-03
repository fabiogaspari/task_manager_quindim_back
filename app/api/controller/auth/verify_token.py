from flask import jsonify
from flask_jwt_extended import jwt_required

from app.api.service.auth.auth_service import AuthService

from . import auth_bp

@auth_bp.route("/verify_token", methods=["GET"])
@jwt_required()
def verify_token() -> jsonify:
    return jsonify(""), 200

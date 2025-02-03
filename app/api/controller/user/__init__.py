from flask import Blueprint

auth_user_bp = Blueprint("users", __name__)

from . import user_controller
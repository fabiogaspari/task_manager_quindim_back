from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from . import login, register, logout, verify_token
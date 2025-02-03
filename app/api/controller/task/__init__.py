from flask import Blueprint

task_auth_bp = Blueprint("tasks", __name__)

from . import task_controller
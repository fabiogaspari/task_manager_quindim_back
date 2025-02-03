from flask import Blueprint

task_status_auth_bp = Blueprint("task_statuses", __name__)

from . import task_status_controller
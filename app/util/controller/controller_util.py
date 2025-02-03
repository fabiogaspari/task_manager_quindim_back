from flask import jsonify
from pydantic import ValidationError
from typing import Callable

class ControllerUtil:
    @staticmethod
    def treat_value_error(exc: ValidationError) -> dict:
        return {err["loc"][0]: err["msg"] for err in exc.errors()}
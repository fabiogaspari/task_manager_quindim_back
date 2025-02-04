from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from app.config.db.mongo_connection import MongoConnection

class TaskStatusModel(BaseModel):
    user: dict
    name: str = Field(..., min_length=3, max_length=64)
    status_color: str = Field(..., min_length=3, max_length=32)
    status_color_font: str = Field(..., min_length=3, max_length=32)
    description: str = Field(..., min_length=3, max_length=128)
    created_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "user": self.user,
            "name": self.name,
            "status_color": self.status_color,
            "status_color_font": self.status_color_font,
            "description": self.description,
            "created_at": self.created_at
        }

    @field_validator('name')
    def unique_name(cls, value):
        user_email = get_jwt_identity()
        if MongoConnection.get_collection('task_status').find_one({"name": value, "user.email": user_email}):
            raise ValueError(f"O nome '{value}' já está em uso.")
        return value
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
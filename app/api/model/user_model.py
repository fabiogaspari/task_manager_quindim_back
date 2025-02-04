from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from app.config.db.mongo_connection import MongoConnection

class UserModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')
    password: str = Field(...)
    is_deactivated: bool = Field(default_factory=False)
    created_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    @field_validator('email')
    def unique_email(cls, value):
        if MongoConnection.get_collection('user').find_one({"email": value}):
            raise ValueError(f"O email '{value}' já está em uso.")
        return value
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
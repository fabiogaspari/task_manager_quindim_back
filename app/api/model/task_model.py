from pydantic import BaseModel, Field
from datetime import datetime

class TaskModel(BaseModel):
    user: dict
    status: dict
    title: str = Field(..., min_length=3, max_length=128)
    expiration_date: datetime | None = Field(default=None)
    created_at: datetime = Field(..., default_factory=None)

    def to_dict(self) -> dict:
        return {
            "user": self.user,
            "status": self.status,
            "title": self.title,
            "expiration_date": self.expiration_date,
            "created_at": self.created_at
        }

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
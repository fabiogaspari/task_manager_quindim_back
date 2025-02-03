from abc import ABC, abstractmethod
from pydantic import BaseModel
from app.util.repository.repository_util import *

class DefaultInterfaceRepository(ABC):
    @abstractmethod
    def create(obj: BaseModel):
        pass

    @abstractmethod
    def get_by_id(id):
        pass
    
    @abstractmethod
    def update(id, data):
        pass

    @abstractmethod
    def delete(id, data):
        pass
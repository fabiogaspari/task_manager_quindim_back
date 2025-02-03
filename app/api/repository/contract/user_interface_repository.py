from abc import ABC, abstractmethod
from pydantic import BaseModel

class UserInterfaceRepository(ABC):
    @abstractmethod
    def create(obj: BaseModel):
        pass

    @abstractmethod
    def get_by_id():
        pass
    
    @abstractmethod
    def update(data):
        pass

    @abstractmethod
    def delete(data):
        pass

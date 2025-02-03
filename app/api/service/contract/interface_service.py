from abc import ABC, abstractmethod

class InterfaceService(ABC):
    @abstractmethod
    def create() -> str:
        pass

    @abstractmethod
    def get_by_id(id) -> ABC:
        pass
    @abstractmethod
    def update(id, update_data) -> bool:
        pass

    @abstractmethod
    def delete(id) -> bool:
        pass

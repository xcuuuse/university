from abc import ABC, abstractmethod
from src.domain.entities.map_object import MapObject

class MapObjectRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[MapObject]:
        pass

    


from src.domain.repositories.map_object_repository import MapObject, MapObjectRepository

class InMemoryMapObjectRepository(MapObjectRepository):
    def __init__(self, map_objects: list[MapObject]):
        self.__map_objects = map_objects

    def get_all(self) -> list[MapObject]:
        return self.__map_objects.copy()


from src.domain.entities.location import Location
from src.domain.entities.parking_space import ParkingSpace

class MapObject:
    def __init__(
            self,
            object_type: str,
            location: Location
    ):
        self.__object_type = object_type
        self.__location = location

    @property
    def object_type(self):
        return self.__object_type

    @property
    def location(self):
        return self.__location

    def find_closest(self) ->  None:
        pass
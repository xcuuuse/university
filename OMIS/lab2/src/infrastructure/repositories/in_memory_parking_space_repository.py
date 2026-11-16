from typing import Optional
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.entities.parking_space import ParkingSpace

class InMemoryParkingSpaceRepository(ParkingSpaceRepository):
    def __init__(self):
        self.__parking_spaces: dict[int, ParkingSpace] = {}

    def get_all(self) -> list[ParkingSpace]:
        return list(self.__parking_spaces.values())

    def get_by_number(self, number: int) -> Optional[ParkingSpace]:
        return self.__parking_spaces.get(number)

    def save(self, space: ParkingSpace) -> None:
        self.__parking_spaces[space.number] = space





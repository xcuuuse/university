from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.parking_space import ParkingSpace

class ParkingSpaceRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[ParkingSpace]:
        pass

    @abstractmethod
    def get_by_number(self, number: int) -> Optional[ParkingSpace]:
        pass

    @abstractmethod
    def save(self, space: ParkingSpace) -> None:
        pass


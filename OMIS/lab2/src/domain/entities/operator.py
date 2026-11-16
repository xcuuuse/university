from src.domain.entities.parking_space import ParkingSpace


class Operator:
    def __init__(self, operator_id: int, name: str):
        self.__id = operator_id
        self.__name = name
        self.__parking_spaces: list[ParkingSpace] = []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def parking_spaces(self) -> list[ParkingSpace]:
        return self.__parking_spaces.copy()

    def add_parking_space(self) -> None:
        pass

    def change_space_info(self) -> None:
        pass
class Location:
    def __init__(
            self,
            pos_x: float,
            pos_y: float,
            coord_system: str
    ):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__coord_system = coord_system

    @property
    def pos_x(self) -> float:
        return self.__pos_x

    @property
    def pos_y(self) -> float:
        return self.__pos_y

    @property
    def coord_system(self) -> str:
        return self.__coord_system


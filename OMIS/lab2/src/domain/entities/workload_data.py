class WorkloadData:
    def __init__(
            self,
            empty_places: int,
            occupied_places: int
    ):
        self.__empty_places = empty_places
        self.__occupied_places = occupied_places

    @property
    def empty_places(self) -> int:
        return self.__empty_places

    @property
    def occupied_places(self) -> int:
        return self.__occupied_places

    def calculate_workload(self) -> float:
        total = self.__empty_places + self.__occupied_places
        if total == 0:
            return 0.0
        return self.__occupied_places / total

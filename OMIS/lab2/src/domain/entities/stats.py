from src.domain.entities.prediction import Prediction


class Statistics:
    def __init__(
            self,
            period: str,
            avg_workload: float = 0.0,
            booking_count: int = 0
    ):
        self.__period = period
        self.__avg_workload = avg_workload
        self.__booking_count = booking_count
        self.__predictions: list[Prediction] = []

    @property
    def period(self) -> str:
        return self.__period

    @property
    def avg_workload(self) -> float:
        return self.__avg_workload

    @property
    def booking_count(self) -> int:
        return self.__booking_count

    @property
    def predictions(self) -> list[Prediction]:
        return self.__predictions.copy()

    def calculate_workload(self) -> float:
        return self.__avg_workload

    def make_report(self) -> None:
        pass
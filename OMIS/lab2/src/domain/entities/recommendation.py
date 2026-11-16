from src.domain.entities.booking import Booking  # зависимость Рекомендация ⇢ Бронь
from src.domain.entities.parking_space import ParkingSpace


class Recommendation:
    def __init__(
            self,
            score: float,
            reason: str,
            parking_space: ParkingSpace
    ):
        self.__score = score
        self.__reason = reason
        self.__parking_space = parking_space

    @property
    def score(self) -> float:
        return self.__score

    @property
    def reason(self) -> str:
        return self.__reason

    @property
    def parking_space(self) -> ParkingSpace:
        return self.__parking_space

    def rate_space(self) -> float:
        return self.__score
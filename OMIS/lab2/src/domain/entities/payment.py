from src.domain.entities.parking_session import ParkingSession

class Payment:
    def __init__(
            self,
            amount: float,
            parking_session: ParkingSession
    ):
        self.__amount = amount
        self.__status: str = "pending"
        self.__parking_session = parking_session

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def parking_session(self) -> ParkingSession:
        return self.__parking_session

    def execute(self) -> None:
        self.__status = "completed"

    def check_status(self) -> str:
        return self.__status


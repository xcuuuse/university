from datetime import datetime, timedelta


class Booking:
    EXTENSION_TIME = timedelta(minutes=30)

    def __init__(
            self,
            start: datetime,
            end: datetime
    ):
        self.__start = start
        self.__end = end
        self.__status = "active"

    @property
    def start(self) -> datetime:
        return self.__start

    @property
    def end(self) -> datetime:
        return self.__end

    @property
    def status(self) -> str:
        return self.__status

    def cancel(self) -> None:
        self.__status = "cancelled"

    def extend(self) -> None:
        self.__end += self.EXTENSION_TIME

    def mark_used(self) -> None:
        self.__status = "used"
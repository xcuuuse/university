from src.domain.entities.booking import Booking
from src.domain.entities.dynamic_pricing import DynamicPricing
from src.domain.entities.location import Location
from src.domain.entities.monitoring_record import MonitoringRecord
from src.domain.entities.parking_session import ParkingSession
from src.domain.entities.space_characteristics import SpaceCharacteristics
from src.domain.entities.stats import Statistics


class ParkingSpace:
    def __init__(
            self,
            number: int,
            price_per_hour: float,
            location: Location,
            status: str = "free"
    ):
        self.__number = number
        self.__status = status
        self.__price_per_hour = price_per_hour
        self.__location = location
        self.__bookings: list[Booking] = []
        self.__parking_sessions: list[ParkingSession] = []
        self.__dynamic_pricing = DynamicPricing(price_per_hour)
        self.__characteristics = SpaceCharacteristics()
        self.__monitoring_records: list[MonitoringRecord] = []
        self.__statistics: list[Statistics] = []

    @property
    def number(self) -> int:
        return self.__number

    @property
    def status(self) -> str:
        return self.__status

    @property
    def price_per_hour(self) -> float:
        return self.__price_per_hour

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def bookings(self) -> list[Booking]:
        return self.__bookings.copy()

    @property
    def parking_sessions(self) -> list[ParkingSession]:
        return self.__parking_sessions.copy()

    @property
    def dynamic_pricing(self) -> DynamicPricing:
        return self.__dynamic_pricing

    @property
    def characteristics(self) -> SpaceCharacteristics:
        return self.__characteristics

    @property
    def monitoring_records(self) -> list[MonitoringRecord]:
        return self.__monitoring_records.copy()

    @property
    def statistics(self) -> list[Statistics]:
        return self.__statistics.copy()

    def occupy(self) -> None:
        self.__status = "occupied"

    def release(self) -> None:
        self.__status = "free"

    def change_status(self, new_status: str) -> None:
        self.__status = new_status

    def update_characteristics(self) -> None:
        pass

    def get_statistics(self, period: str) -> Statistics:
        statistics = Statistics(period, booking_count=len(self.__bookings))
        self.__statistics.append(statistics)
        return statistics

    def add_booking(self, booking: Booking) -> None:
        self.__bookings.append(booking)

    def add_session(self, session: ParkingSession) -> None:
        self.__parking_sessions.append(session)


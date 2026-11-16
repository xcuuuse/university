from typing import Optional

from src.domain.entities.booking import Booking
from src.domain.entities.location import Location
from src.domain.entities.parking_session import ParkingSession
from src.domain.entities.wallet import Wallet
from src.domain.entities.recommendation import Recommendation


class User:
    def __init__(
            self,
            user_id: int,
            name: str,
            location: Optional[Location] = None
    ):
        self.__id = user_id
        self.__name = name
        self.__location = location
        self.__wallet = Wallet()
        self.__bookings: list[Booking] = []
        self.__parking_sessions: list[ParkingSession] = []
        self.__recommendations: list[Recommendation] = []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def location(self) -> Optional[Location]:
        return self.__location

    @property
    def wallet(self) -> Wallet:
        return self.__wallet

    @property
    def bookings(self) -> list[Booking]:
        return self.__bookings.copy()

    @property
    def parking_sessions(self) -> list[ParkingSession]:
        return self.__parking_sessions.copy()

    def update_location(self) -> None:
        pass

    def get_recommendations(self) -> list[Recommendation]:
        return self.__recommendations.copy()

    def add_booking(self, booking: Booking) -> None:
        self.__bookings.append(booking)

    def change_name(self, new_name: str) -> None:
        self.__name =  new_name

    def add_session(self, session: ParkingSession) -> None:
        self.__parking_sessions.append(session)

    

from datetime import datetime
from typing import Optional

from src.application.exceptions import (
    ActiveSessionExistsError,
    NoActiveSessionError,
    SpaceUnavailableError,
)
from src.application.helpers import (
    find_active_booking,
    find_active_session,
    find_space_by_session,
    get_space_or_raise,
    get_user_or_raise,
    session_cost,
)
from src.domain.entities.parking_session import ParkingSession
from src.domain.entities.parking_space import ParkingSpace
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.repositories.user_repository import UserRepository


class OccupancyService:
    def __init__(
            self,
            user_repo: UserRepository,
            parking_repo: ParkingSpaceRepository
    ):
        self.__user_repo = user_repo
        self.__parking_repo = parking_repo

    def occupy(self, user_id: int, space_number: int) -> ParkingSession:
        user = get_user_or_raise(self.__user_repo, user_id)
        space = get_space_or_raise(self.__parking_repo, space_number)
        if find_active_session(user) is not None:
            raise ActiveSessionExistsError()
        booking = find_active_booking(user)
        booked_by_user = (
            space.status == "booked"
            and booking is not None
            and booking in space.bookings
        )
        if space.status != "free" and not booked_by_user:
            raise SpaceUnavailableError("Место занято или забронировано другим пользователем")
        if booked_by_user:
            booking.mark_used()
        space.occupy()
        session = ParkingSession(datetime.now())
        user.add_session(session)
        space.add_session(session)
        self.__user_repo.save(user)
        self.__parking_repo.save(space)
        return session

    def current_session(self, user_id: int) -> Optional[tuple[ParkingSpace, ParkingSession]]:
        user = get_user_or_raise(self.__user_repo, user_id)
        session = find_active_session(user)
        if session is None:
            return None
        space = find_space_by_session(self.__parking_repo, session)
        if space is None:
            return None
        return space, session

    def session_details(self, user_id: int) -> dict:
        current = self.current_session(user_id)
        if current is None:
            raise NoActiveSessionError()
        space, session = current
        return {
            "space_number": space.number,
            "start_time": session.start_time,
            "duration_hours": session.calculate_duration(),
            "cost": session_cost(session, space),
        }

    def release(self, user_id: int) -> ParkingSession:
        user = get_user_or_raise(self.__user_repo, user_id)
        current = self.current_session(user_id)
        if current is None:
            raise NoActiveSessionError()
        space, session = current
        session.complete()
        space.release()
        self.__user_repo.save(user)
        self.__parking_repo.save(space)
        return session
import math
from typing import Optional

from src.application.exceptions import SpaceNotFoundError, UserNotFoundError
from src.domain.entities.booking import Booking
from src.domain.entities.location import Location
from src.domain.entities.parking_session import ParkingSession
from src.domain.entities.parking_space import ParkingSpace
from src.domain.entities.user import User
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.repositories.user_repository import UserRepository

BASE_POINT = Location(53.9023, 27.5619, "WGS84")


def get_user_or_raise(repo: UserRepository, user_id: int) -> User:
    user = repo.get_by_id(user_id)
    if user is None:
        raise UserNotFoundError()
    return user


def get_space_or_raise(repo: ParkingSpaceRepository, number: int) -> ParkingSpace:
    space = repo.get_by_number(number)
    if space is None:
        raise SpaceNotFoundError()
    return space


def start_point(user: User) -> Location:
    return user.location or BASE_POINT


def distance(a: Location, b: Location) -> float:
    return math.hypot(a.pos_x - b.pos_x, a.pos_y - b.pos_y)


def find_active_booking(user: User) -> Optional[Booking]:
    for booking in user.bookings:
        if booking.status == "active":
            return booking
    return None


def find_active_session(user: User) -> Optional[ParkingSession]:
    for session in user.parking_sessions:
        if session.end_time is None:
            return session
    return None


def find_space_by_booking(
        repo: ParkingSpaceRepository,
        booking: Booking) -> Optional[ParkingSpace]:
    for space in repo.get_all():
        if booking in space.bookings:
            return space
    return None


def find_space_by_session(
        repo: ParkingSpaceRepository,
        session: ParkingSession) -> Optional[ParkingSpace]:
    for space in repo.get_all():
        if session in space.parking_sessions:
            return space
    return None


def session_cost(session: ParkingSession, space: ParkingSpace) -> float:
    return round(session.calculate_duration() * space.price_per_hour, 2)
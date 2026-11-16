from datetime import datetime
from typing import Optional

from src.application.exceptions import (
    ActiveBookingExistsError,
    NoActiveBookingError,
    SpaceUnavailableError,
    ValidationError,
)
from src.application.helpers import (
    find_active_booking,
    find_space_by_booking,
    get_space_or_raise,
    get_user_or_raise,
)
from src.domain.entities.booking import Booking
from src.domain.entities.parking_space import ParkingSpace
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.repositories.user_repository import UserRepository


class BookingService:
    def __init__(
            self,
            user_repo: UserRepository,
            parking_repo: ParkingSpaceRepository
    ):
        self.__user_repo = user_repo
        self.__parking_repo = parking_repo

    def book(
            self,
            user_id: int,
            space_number: int,
            start: datetime,
            end: datetime
    ) -> Booking:
        if start >= end:
            raise ValidationError("Время начала должно быть раньше времени окончания")
        if end <= datetime.now():
            raise ValidationError("Время окончания брони уже прошло")
        user = get_user_or_raise(self.__user_repo, user_id)
        space = get_space_or_raise(self.__parking_repo, space_number)
        if find_active_booking(user) is not None:
            raise ActiveBookingExistsError()
        if space.status != "free":
            raise SpaceUnavailableError("Место уже занято или забронировано")
        booking = Booking(start, end)
        user.add_booking(booking)
        space.add_booking(booking)
        space.change_status("booked")
        self.__user_repo.save(user)
        self.__parking_repo.save(space)
        return booking

    def extend(self, user_id: int) -> Booking:
        user = get_user_or_raise(self.__user_repo, user_id)
        booking = self.__get_active_booking_or_raise(user_id)
        booking.extend()
        self.__user_repo.save(user)
        return booking

    def cancel(self, user_id: int) -> None:
        user = get_user_or_raise(self.__user_repo, user_id)
        booking = self.__get_active_booking_or_raise(user_id)
        booking.cancel()

        space = find_space_by_booking(self.__parking_repo, booking)
        if space is not None:
            space.release()
            self.__parking_repo.save(space)
        self.__user_repo.save(user)

    def current_booking(self, user_id: int) -> Optional[tuple[ParkingSpace, Booking]]:
        user = get_user_or_raise(self.__user_repo, user_id)
        booking = find_active_booking(user)
        if booking is None:
            return None
        space = find_space_by_booking(self.__parking_repo, booking)
        if space is None:
            return None
        return space, booking

    def __get_active_booking_or_raise(self, user_id: int) -> Booking:
        booking = find_active_booking(get_user_or_raise(self.__user_repo, user_id))
        if booking is None:
            raise NoActiveBookingError()
        return booking
from typing import Optional
from src.application.exceptions import InsufficientFundsError, NoActiveSessionError
from src.application.helpers import (
    find_active_session,
    find_space_by_session,
    get_user_or_raise,
    session_cost,
)
from src.domain.entities.parking_session import ParkingSession
from src.domain.entities.parking_space import ParkingSpace
from src.domain.entities.payment import Payment
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.repositories.user_repository import UserRepository


class PaymentService:
    def __init__(
            self,
            user_repo: UserRepository,
            parking_repo: ParkingSpaceRepository
    ):
        self.__user_repo = user_repo
        self.__parking_repo = parking_repo

    def calculate_cost(self, user_id: int) -> float:
        session, space = self.__get_session_and_space(user_id)
        return session_cost(session, space)

    def is_payment_required(self, user_id: int) -> bool:
        _, space = self.__get_session_and_space(user_id)
        return space.price_per_hour > 0

    def pay(self, user_id: int) -> Optional[Payment]:
        user = get_user_or_raise(self.__user_repo, user_id)
        session, space = self.__get_session_and_space(user_id)
        amount = session_cost(session, space)
        if amount <= 0:
            return None
        payment = Payment(amount, session)
        if not user.wallet.debit_funds(amount):
            raise InsufficientFundsError(
                f"Недостаточно средств: нужно {amount:.2f} BYN, "
                f"на счёте {user.wallet.balance:.2f} BYN"
            )
        payment.execute()
        user.wallet.add_payment(payment)
        self.__user_repo.save(user)
        return payment

    def __get_session_and_space(self, user_id: int) -> tuple[ParkingSession, ParkingSpace]:
        user = get_user_or_raise(self.__user_repo, user_id)
        session = find_active_session(user)
        if session is None:
            raise NoActiveSessionError()
        space = find_space_by_session(self.__parking_repo, session)
        if space is None:
            raise NoActiveSessionError()
        return session, space
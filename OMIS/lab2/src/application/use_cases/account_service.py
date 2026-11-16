from src.application.exceptions import ValidationError
from src.application.helpers import get_user_or_raise
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class AccountService:
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def get_user(self, user_id: int) -> User:
        return get_user_or_raise(self.__user_repo, user_id)

    def change_name(self, user_id: int, new_name: str) -> None:
        new_name = new_name.strip()
        if not new_name:
            raise ValidationError("Имя не может быть пустым")
        user = self.get_user(user_id)
        user.change_name(new_name)
        self.__user_repo.save(user)

    def get_balance(self, user_id: int) -> float:
        return self.get_user(user_id).wallet.balance

    def top_up_wallet(self, user_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValidationError("Сумма пополнения должна быть больше нуля")
        user = self.get_user(user_id)
        user.wallet.top_up(amount)
        self.__user_repo.save(user)
        return user.wallet.balance
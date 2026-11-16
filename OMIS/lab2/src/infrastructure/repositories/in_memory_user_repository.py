from typing import Optional
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user import User



class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.__users: dict[int, User] = {}

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.__users.get(user_id)

    def save(self, user: User) -> None:
        self.__users[user.id] = user







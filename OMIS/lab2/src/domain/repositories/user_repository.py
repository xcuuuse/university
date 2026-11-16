from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass


from src.application.helpers import get_user_or_raise, start_point
from src.domain.entities.location import Location
from src.domain.repositories.user_repository import UserRepository


class RouteService:
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def build_route(self, user_id: int, destination: Location) -> list[Location]:
        user = get_user_or_raise(self.__user_repo, user_id)
        return [start_point(user), destination]
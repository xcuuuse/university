from src.domain.entities.location import Location
from src.application.helpers import distance, get_space_or_raise, get_user_or_raise, start_point
from src.domain.entities.map_object import MapObject
from src.domain.entities.parking_space import ParkingSpace
from src.domain.repositories.map_object_repository import MapObjectRepository
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.repositories.user_repository import UserRepository


class MapService:
    def __init__(
            self,
            user_repo: UserRepository,
            parking_repo: ParkingSpaceRepository,
            map_object_repo: MapObjectRepository
    ):
        self.__user_repo = user_repo
        self.__parking_repo = parking_repo
        self.__map_object_repo = map_object_repo

    def nearest_spaces(self, user_id: int, amount: int = 5) -> list[ParkingSpace]:
        point = start_point(get_user_or_raise(self.__user_repo, user_id))
        spaces = sorted(
            self.__parking_repo.get_all(),
            key=lambda space: distance(point, space.location)
        )
        return spaces[:amount]

    def is_location_defined(self, user_id: int) -> bool:
        return get_user_or_raise(self.__user_repo, user_id).location is not None

    def map_objects(self) -> list[MapObject]:
        return self.__map_object_repo.get_all()

    def space_info(self, number: int) -> ParkingSpace:
        return get_space_or_raise(self.__parking_repo, number)

    def all_spaces(self) -> list[ParkingSpace]:
        return self.__parking_repo.get_all()

    def start_point(self, user_id: int) -> Location:
        return start_point(get_user_or_raise(self.__user_repo, user_id))
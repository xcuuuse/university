from src.domain.entities.location import Location
from src.domain.entities.map_object import MapObject
from src.domain.entities.parking_space import ParkingSpace
from src.domain.entities.user import User
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository
from src.domain.repositories.user_repository import UserRepository

COORD_SYSTEM = "WGS84"


DEFAULT_USER_ID = 123123123  # id устройства с макета аккаунта


def seed_users(repository: UserRepository) -> None:
    user = User(DEFAULT_USER_ID, "Жанна")
    user.wallet.top_up(45.67)
    repository.save(user)


def seed_parking_spaces(repository: ParkingSpaceRepository) -> None:
    spaces = [
        ParkingSpace(6769, 0.0, Location(53.9185, 27.5937, COORD_SYSTEM)),
        ParkingSpace(1234, 2.0, Location(53.9065, 27.5520, COORD_SYSTEM)),
        ParkingSpace(4321, 1.5, Location(53.9310, 27.6480, COORD_SYSTEM), status="occupied"),
        ParkingSpace(5050, 3.0, Location(53.8950, 27.5480, COORD_SYSTEM)),
    ]
    for space in spaces:
        repository.save(space)


def create_map_objects() -> list[MapObject]:
    return [
        MapObject("gas_station", Location(53.9120, 27.5830, COORD_SYSTEM)),
        MapObject("gas_station", Location(53.8890, 27.6150, COORD_SYSTEM)),
        MapObject("car_wash", Location(53.9250, 27.5710, COORD_SYSTEM)),
    ]
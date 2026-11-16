"""Точка входа и точка сборки приложения.

Единственное место, которое знает обо всех слоях: создаёт конкретные репозитории
(infrastructure), передаёт их сервисам (application), а сервисы — окну (presentation).
"""
import sys

from PyQt6.QtWidgets import QApplication

from src.application.use_cases.account_service import AccountService
from src.application.use_cases.booking_service import BookingService
from src.application.use_cases.map_service import MapService
from src.application.use_cases.occupancy_service import OccupancyService
from src.application.use_cases.payment_service import PaymentService
from src.application.use_cases.route_service import RouteService
from src.infrastructure.repositories.in_memory_map_object_repository import InMemoryMapObjectRepository
from src.infrastructure.repositories.in_memory_parking_space_repository import InMemoryParkingSpaceRepository
from src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from src.infrastructure.seed_data import DEFAULT_USER_ID, create_map_objects, seed_parking_spaces, seed_users
from src.presentation.windows.main_window import MainWindow


def main() -> None:
    # infrastructure: хранилища и тестовые данные
    user_repo = InMemoryUserRepository()
    parking_repo = InMemoryParkingSpaceRepository()
    map_object_repo = InMemoryMapObjectRepository(create_map_objects())
    seed_users(user_repo)
    seed_parking_spaces(parking_repo)

    # application: сервисы получают абстрактные репозитории
    map_service = MapService(user_repo, parking_repo, map_object_repo)
    booking_service = BookingService(user_repo, parking_repo)
    occupancy_service = OccupancyService(user_repo, parking_repo)
    payment_service = PaymentService(user_repo, parking_repo)
    route_service = RouteService(user_repo)
    account_service = AccountService(user_repo)

    # presentation: окно получает сервисы
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow(
        DEFAULT_USER_ID,
        map_service, booking_service, occupancy_service,
        payment_service, route_service, account_service,
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

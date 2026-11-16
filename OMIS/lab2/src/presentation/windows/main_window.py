from datetime import datetime
from typing import Optional

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QScrollArea, QStackedWidget, QVBoxLayout, QWidget,
)

from src.application.use_cases.account_service import AccountService
from src.application.use_cases.booking_service import BookingService
from src.application.use_cases.map_service import MapService
from src.application.use_cases.occupancy_service import OccupancyService
from src.application.use_cases.payment_service import PaymentService
from src.application.use_cases.route_service import RouteService
from src.domain.entities.location import Location
from src.domain.entities.parking_space import ParkingSpace
from src.presentation import styles
from src.presentation.error_handling import safe_call
from src.presentation.widgets.buttons import BaseButton
from src.presentation.widgets.map_widget import MapWidget
from src.presentation.widgets.side_menu import SideMenu
from src.presentation.widgets.space_card import SpaceCard
from src.presentation.widgets.status_panel import StatusPanel
from src.presentation.windows.account_screen import AccountScreen
from src.presentation.windows.booking_dialog import BookingDialog
from src.presentation.windows.change_name_dialog import ChangeNameDialog
from src.presentation.windows.profile_edit_screen import ProfileEditScreen
from src.presentation.windows.settings_screen import SettingsScreen
from src.presentation.windows.top_up_dialog import TopUpDialog
from src.presentation.windows.wallet_screen import WalletScreen


class MainWindow(QMainWindow):
    """Пользовательский интерфейс из модели (класс «ПользовательскийИнтерфейс»).

    Хранит все экраны в QStackedWidget и переключает их по диаграмме состояний.
    Сам ничего не вычисляет: все действия идут через сервисы слоя application.
    """

    WINDOW_SIZE = (420, 800)
    STATUS_REFRESH_MS = 5000

    def __init__(
            self,
            user_id: int,
            map_service: MapService,
            booking_service: BookingService,
            occupancy_service: OccupancyService,
            payment_service: PaymentService,
            route_service: RouteService,
            account_service: AccountService
    ):
        super().__init__()
        self.__user_id = user_id
        self.__map_service = map_service
        self.__booking_service = booking_service
        self.__occupancy_service = occupancy_service
        self.__payment_service = payment_service
        self.__route_service = route_service
        self.__account_service = account_service

        # Связи из модели: Карта (1), Кнопка (*), Местоположение (*)
        self.__map = MapWidget("Минск")
        self.__buttons: list[BaseButton] = []
        self.__locations: list[Location] = []

        self.__selected_number: Optional[int] = None

        self.draw_interface()

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__refresh_status_panel)
        self.__timer.start(self.STATUS_REFRESH_MS)

    # ================= методы из модели =================

    def draw_interface(self) -> None:
        """Собирает окно целиком: главный экран, страницы меню и формы."""
        self.setWindowTitle("Парковки Минска")
        self.setFixedSize(*self.WINDOW_SIZE)

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.__stack = QStackedWidget()
        root_layout.addWidget(self.__stack)
        self.setCentralWidget(root)

        self.__account_screen = AccountScreen(self.show_main, self.show_profile_edit)
        self.__profile_edit_screen = ProfileEditScreen(self.show_account, self.__open_change_name)
        self.__wallet_screen = WalletScreen(self.show_main, self.__open_top_up)
        self.__settings_screen = SettingsScreen(self.show_main)

        self.__main_page = self.__build_main_page()
        for page in (self.__main_page, self.__account_screen, self.__profile_edit_screen,
                     self.__wallet_screen, self.__settings_screen):
            self.__stack.addWidget(page)

        # Формы и меню лежат поверх любого экрана
        self.__side_menu = SideMenu(root, self.show_account, self.show_wallet, self.show_settings)
        self.__booking_dialog = BookingDialog(root, self.__confirm_booking)
        self.__change_name_dialog = ChangeNameDialog(root, self.__confirm_change_name, self.show_account)
        self.__top_up_dialog = TopUpDialog(root, self.__confirm_top_up)

        self.draw_button()
        self.show_main()

    def display_map(self) -> None:
        """Передаёт карте места, заправки и мойки."""
        self.__map.set_spaces(self.__map_service.all_spaces())
        self.__map.set_map_objects(self.__map_service.map_objects())
        self.__map.set_selected(self.__selected_number)

    def draw_button(self) -> None:
        """Рисует кнопку «бургер» поверх карты."""
        burger = BaseButton("☰", 44, 44, styles.DARK_BLUE, self.__side_menu.open)
        burger.setStyleSheet(burger.styleSheet() + "QPushButton { color: white; font-size: 20px; }")
        self.__buttons.append(burger)
        self.__map_area_layout.addWidget(
            burger, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

    def display_location(self) -> None:
        """Показывает точку пользователя или базовую точку (развилка при открытии приложения)."""
        point = self.__map_service.start_point(self.__user_id)
        defined = self.__map_service.is_location_defined(self.__user_id)
        self.__locations = [point]
        self.__map.set_user_point(point, defined)
        self.__list_caption.setText(
            "Ближайшие места" if defined
            else "Геолокация не определена: места от базовой точки"
        )

    # ================= навигация =================

    def show_main(self) -> None:
        self.__side_menu.close_overlay()
        self.__refresh_main()
        self.__stack.setCurrentWidget(self.__main_page)

    def show_account(self) -> None:
        self.__side_menu.close_overlay()
        self.__account_screen.show_user(self.__account_service.get_user(self.__user_id))
        self.__stack.setCurrentWidget(self.__account_screen)

    def show_profile_edit(self) -> None:
        self.__side_menu.close_overlay()
        self.__stack.setCurrentWidget(self.__profile_edit_screen)

    def show_wallet(self) -> None:
        self.__side_menu.close_overlay()
        self.__wallet_screen.show_balance(self.__account_service.get_balance(self.__user_id))
        self.__stack.setCurrentWidget(self.__wallet_screen)

    def show_settings(self) -> None:
        self.__side_menu.close_overlay()
        self.__stack.setCurrentWidget(self.__settings_screen)

    # ================= главный экран =================

    def __build_main_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Карта, а поверх неё бургер и плашка статуса (виджеты в одной ячейке сетки)
        map_area = QWidget()
        self.__map_area_layout = QGridLayout(map_area)
        self.__map_area_layout.setContentsMargins(0, 0, 0, 0)
        self.__map_area_layout.addWidget(self.__map, 0, 0)
        self.__map.space_clicked.connect(self.__select_space)

        self.__status_panel = StatusPanel(
            on_occupy=self.__occupy_booked,
            on_extend=self.__extend_booking,
            on_cancel=self.__cancel_booking,
            on_release=self.__release,
        )
        status_holder = QWidget()
        holder_layout = QVBoxLayout(status_holder)
        holder_layout.setContentsMargins(0, 62, 0, 0)
        holder_layout.addWidget(self.__status_panel, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.__map_area_layout.addWidget(
            status_holder, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        # Лента карточек мест под картой
        bottom = QFrame()
        bottom.setObjectName("bottom")
        bottom.setStyleSheet(f"QFrame#bottom {{ {styles.DARK_BACKGROUND} }}")
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(10, 8, 10, 10)
        self.__list_caption = QLabel()
        self.__list_caption.setStyleSheet(f"color: {styles.TEXT_LIGHT}; font-size: 11px;")
        bottom_layout.addWidget(self.__list_caption)

        self.__cards_scroll = QScrollArea()
        self.__cards_scroll.setWidgetResizable(True)
        self.__cards_scroll.setFixedHeight(170)
        self.__cards_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__cards_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        bottom_layout.addWidget(self.__cards_scroll)

        layout.addWidget(map_area, stretch=1)
        layout.addWidget(bottom)
        return page

    def __refresh_main(self) -> None:
        self.display_map()
        self.display_location()
        self.__refresh_status_panel()
        self.__refresh_cards()

    def __refresh_status_panel(self) -> None:
        session = self.__occupancy_service.current_session(self.__user_id)
        if session is not None:
            details = self.__occupancy_service.session_details(self.__user_id)
            self.__status_panel.show_occupied(
                details["space_number"], details["start_time"],
                details["duration_hours"], details["cost"],
            )
            return
        booking = self.__booking_service.current_booking(self.__user_id)
        if booking is not None:
            space, current = booking
            self.__status_panel.show_booked(space.number, current.end)
            return
        self.__status_panel.hide()

    def __refresh_cards(self) -> None:
        """Пересобирает ленту карточек. Старый контейнер QScrollArea удаляет сам."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        cards_layout = QHBoxLayout(container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(10)

        has_session = self.__occupancy_service.current_session(self.__user_id) is not None
        booking = self.__booking_service.current_booking(self.__user_id)
        booked_number = booking[0].number if booking else None

        for space in self.__map_service.nearest_spaces(self.__user_id, amount=10):
            cards_layout.addWidget(SpaceCard(
                space,
                can_occupy=self.__can_occupy(space, has_session, booked_number),
                can_book=booking is None and space.status == "free",
                selected=space.number == self.__selected_number,
                on_occupy=self.__occupy,
                on_book=self.__booking_dialog.open_for,
                on_select=self.__select_space,
            ))
        cards_layout.addStretch()
        self.__cards_scroll.setWidget(container)

    @staticmethod
    def __can_occupy(space: ParkingSpace, has_session: bool, booked_number: Optional[int]) -> bool:
        if has_session:
            return False
        return space.status == "free" or space.number == booked_number

    # ================= обработчики действий =================

    def __select_space(self, number: int) -> None:
        """Выбор места на карте или в ленте: подсветка и маршрут до него (подсистемы 1 и 6)."""
        ok, space = safe_call(self, self.__map_service.space_info, number)
        if not ok:
            return
        self.__selected_number = number
        ok, route = safe_call(self, self.__route_service.build_route, self.__user_id, space.location)
        if ok:
            self.__map.set_route(route)
        self.__refresh_main()

    def __confirm_booking(self, number: int, start: datetime, end: datetime) -> bool:
        ok, _ = safe_call(self, self.__booking_service.book, self.__user_id, number, start, end)
        if ok:
            self.__refresh_main()
        return ok

    def __occupy(self, number: int) -> None:
        ok, _ = safe_call(self, self.__occupancy_service.occupy, self.__user_id, number)
        if ok:
            self.__refresh_main()

    def __occupy_booked(self) -> None:
        booking = self.__booking_service.current_booking(self.__user_id)
        if booking is not None:
            self.__occupy(booking[0].number)

    def __extend_booking(self) -> None:
        ok, booking = safe_call(self, self.__booking_service.extend, self.__user_id)
        if ok:
            self.__refresh_main()
            QMessageBox.information(
                self, "Бронь продлена",
                f"Бронь продлена до {styles.format_datetime(booking.end)}"
            )

    def __cancel_booking(self) -> None:
        ok, _ = safe_call(self, self.__booking_service.cancel, self.__user_id)
        if ok:
            self.__refresh_main()

    def __release(self) -> None:
        """Освобождение места: сначала оплата (если место платное), потом освобождение."""
        ok, required = safe_call(self, self.__payment_service.is_payment_required, self.__user_id)
        if not ok:
            return
        if required:
            ok, cost = safe_call(self, self.__payment_service.calculate_cost, self.__user_id)
            if not ok or not self.__ask_payment(cost):
                return
            ok, _ = safe_call(self, self.__payment_service.pay, self.__user_id)
            if not ok:
                return
        ok, _ = safe_call(self, self.__occupancy_service.release, self.__user_id)
        if ok:
            self.__map.set_route([])
            self.__selected_number = None
            self.__refresh_main()

    def __ask_payment(self, cost: float) -> bool:
        box = QMessageBox(self)
        box.setWindowTitle("Оплата парковки")
        box.setText(f"Стоимость парковки: {cost:.2f} BYN.\nОплатить с кошелька?")
        pay_button = box.addButton("Оплатить", QMessageBox.ButtonRole.AcceptRole)
        box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
        box.exec()
        return box.clickedButton() is pay_button

    # ----- аккаунт и кошелёк -----

    def __open_change_name(self) -> None:
        self.__change_name_dialog.open()

    def __confirm_change_name(self, name: str) -> bool:
        ok, _ = safe_call(self, self.__account_service.change_name, self.__user_id, name)
        return ok

    def __open_top_up(self) -> None:
        self.__top_up_dialog.open()

    def __confirm_top_up(self, amount: float) -> bool:
        ok, balance = safe_call(self, self.__account_service.top_up_wallet, self.__user_id, amount)
        if ok:
            self.__wallet_screen.show_balance(balance)
        return ok

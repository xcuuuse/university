import math
from typing import Optional

from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QWidget

from src.domain.entities.location import Location
from src.domain.entities.map_object import MapObject
from src.domain.entities.parking_space import ParkingSpace
from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton

CITY_CENTER = (53.905, 27.565)
RIVER = [(53.950, 27.460), (53.935, 27.510), (53.918, 27.540), (53.906, 27.553),
         (53.898, 27.580), (53.888, 27.615), (53.872, 27.660), (53.860, 27.700)]
PARKS = [((53.925, 27.590), 0.007, 0.013), ((53.885, 27.540), 0.006, 0.012),
         ((53.940, 27.620), 0.008, 0.010), ((53.895, 27.640), 0.005, 0.011)]
AVENUES = [[(53.860, 27.480), (53.905, 27.565), (53.960, 27.700)],
           [(53.950, 27.470), (53.905, 27.565), (53.865, 27.690)],
           [(53.905, 27.450), (53.905, 27.720)],
           [(53.850, 27.565), (53.960, 27.565)]]
MAP_BACKGROUND = QColor("#F2F1EC")


class MapWidget(QWidget):
    space_clicked = pyqtSignal(int)
    MIN_ZOOM = 0.6
    MAX_ZOOM = 4.0
    MARKER_RADIUS = 19
    def __init__(self, source: str = "Минск", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__source = source
        self.__spaces: list[ParkingSpace] = []
        self.__map_objects: list[MapObject] = []
        self.__user_point: Optional[Location] = None
        self.__location_defined = False
        self.__route: list[Location] = []
        self.__selected_number: Optional[int] = None

        self.__zoom = 1.0
        self.__center_lat, self.__center_lon = 53.908, 27.585
        self.__press_pos: Optional[QPointF] = None
        self.__dragged = False

        self.setMinimumHeight(300)
        self.setMouseTracking(True)

        self.__zoom_in_button = BaseButton("+", 36, 36, styles.CARD_GREY, self.zoom_in, self)
        self.__zoom_out_button = BaseButton("−", 36, 36, styles.CARD_GREY, self.zoom_out, self)

    @property
    def source(self) -> str:
        return self.__source

    # ---------- данные для отрисовки ----------

    def set_spaces(self, spaces: list[ParkingSpace]) -> None:
        self.__spaces = list(spaces)
        self.update()

    def set_map_objects(self, map_objects: list[MapObject]) -> None:
        self.__map_objects = list(map_objects)
        self.update()

    def set_user_point(self, point: Location, location_defined: bool) -> None:
        self.__user_point = point
        self.__location_defined = location_defined
        self.update()

    def set_route(self, route: list[Location]) -> None:
        self.__route = list(route)
        self.update()

    def set_selected(self, number: Optional[int]) -> None:
        self.__selected_number = number
        self.update()

    # ---------- масштаб ----------

    def zoom_in(self) -> None:
        self.__set_zoom(self.__zoom * 1.25)

    def zoom_out(self) -> None:
        self.__set_zoom(self.__zoom / 1.25)

    def __set_zoom(self, value: float) -> None:
        self.__zoom = max(self.MIN_ZOOM, min(self.MAX_ZOOM, value))
        self.update()

    # ---------- перевод координат ----------

    def __scale(self) -> float:
        """Пикселей на градус широты."""
        cos_lat = math.cos(math.radians(self.__center_lat))
        base = min(self.height() / 0.10, self.width() / (0.18 * cos_lat))
        return base * self.__zoom

    def __to_screen(self, lat: float, lon: float) -> QPointF:
        k = self.__scale()
        cos_lat = math.cos(math.radians(self.__center_lat))
        x = self.width() / 2 + (lon - self.__center_lon) * k * cos_lat
        y = self.height() / 2 - (lat - self.__center_lat) * k
        return QPointF(x, y)

    def __location_to_screen(self, location: Location) -> QPointF:
        return self.__to_screen(location.pos_x, location.pos_y)

    # ---------- отрисовка ----------

    def resizeEvent(self, event) -> None:
        self.__zoom_in_button.move(self.width() - 48, self.height() - 96)
        self.__zoom_out_button.move(self.width() - 48, self.height() - 54)
        super().resizeEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), MAP_BACKGROUND)

        self.__draw_background(painter)
        self.__draw_route(painter)
        self.__draw_map_objects(painter)
        self.__draw_spaces(painter)
        self.__draw_user_point(painter)
        painter.end()

    def __draw_background(self, painter: QPainter) -> None:
        k = self.__scale()
        cos_lat = math.cos(math.radians(self.__center_lat))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#CDEBB5"))
        for (lat, lon), r_lat, r_lon in PARKS:
            center = self.__to_screen(lat, lon)
            painter.drawEllipse(center, r_lon * k * cos_lat, r_lat * k)

        street_pen = QPen(QColor("#C3C8D4"), max(2.0, 3 * self.__zoom))
        street_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(street_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for r_lat, r_lon in ((0.018, 0.030), (0.035, 0.060), (0.058, 0.098)):
            center = self.__to_screen(*CITY_CENTER)
            painter.drawEllipse(center, r_lon * k * cos_lat, r_lat * k)

        painter.setPen(QPen(QColor("#B4BAC8"), max(3.0, 4 * self.__zoom)))
        for avenue in AVENUES:
            self.__draw_polyline(painter, avenue)

        painter.setPen(QPen(QColor("#8EC9F5"), max(4.0, 6 * self.__zoom)))
        self.__draw_polyline(painter, RIVER)

        painter.setPen(QColor("#5A5F70"))
        painter.setFont(QFont("Sans", int(14 * min(self.__zoom, 1.6)), QFont.Weight.Bold))
        label = self.__to_screen(CITY_CENTER[0] + 0.030, CITY_CENTER[1] - 0.040)
        painter.drawText(label, self.__source)

    def __draw_polyline(self, painter: QPainter, points: list[tuple[float, float]]) -> None:
        path = QPainterPath(self.__to_screen(*points[0]))
        for lat, lon in points[1:]:
            path.lineTo(self.__to_screen(lat, lon))
        painter.drawPath(path)

    def __draw_route(self, painter: QPainter) -> None:
        if len(self.__route) < 2:
            return
        pen = QPen(QColor(styles.DARK_BLUE), 3, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        points = [self.__location_to_screen(point) for point in self.__route]
        for start, end in zip(points, points[1:]):
            painter.drawLine(start, end)

    def __draw_map_objects(self, painter: QPainter) -> None:
        letters = {"gas_station": "А", "car_wash": "М"}
        painter.setFont(QFont("Sans", 9, QFont.Weight.Bold))
        for map_object in self.__map_objects:
            center = self.__location_to_screen(map_object.location)
            rect = QRectF(center.x() - 10, center.y() - 10, 20, 20)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#2D7FF9"))
            painter.drawRoundedRect(rect, 5, 5)
            painter.setPen(QColor("white"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter,
                             letters.get(map_object.object_type, "?"))

    def __draw_spaces(self, painter: QPainter) -> None:
        painter.setFont(QFont("Sans", 7, QFont.Weight.Bold))
        r = self.MARKER_RADIUS
        for space in self.__spaces:
            center = self.__location_to_screen(space.location)
            selected = space.number == self.__selected_number
            painter.setPen(QPen(QColor("white") if selected else QColor(styles.DARK_BLUE), 5))
            painter.setBrush(QBrush(QColor(styles.STATUS_COLORS.get(space.status, styles.BUTTON_BLUE))))
            painter.drawEllipse(center, r, r)
            painter.setPen(QColor(styles.TEXT_DARK))
            painter.drawText(QRectF(center.x() - r, center.y() - r, 2 * r, 2 * r),
                             Qt.AlignmentFlag.AlignCenter, str(space.number))

    def __draw_user_point(self, painter: QPainter) -> None:
        if self.__user_point is None:
            return
        center = self.__location_to_screen(self.__user_point)
        painter.setPen(QPen(QColor("white"), 3))
        painter.setBrush(QColor("#E5484D" if not self.__location_defined else "#1E88E5"))
        painter.drawEllipse(center, 8, 8)
        painter.setPen(QColor(styles.TEXT_DARK))
        painter.setFont(QFont("Sans", 8))
        caption = "Вы здесь" if self.__location_defined else "Базовая точка"
        painter.drawText(QPointF(center.x() + 11, center.y() + 4), caption)

    def mousePressEvent(self, event) -> None:
        self.__press_pos = event.position()
        self.__dragged = False

    def mouseMoveEvent(self, event) -> None:
        if self.__press_pos is None:
            return
        delta = event.position() - self.__press_pos
        if abs(delta.x()) + abs(delta.y()) > 3:
            self.__dragged = True
        if self.__dragged:
            k = self.__scale()
            cos_lat = math.cos(math.radians(self.__center_lat))
            self.__center_lon -= delta.x() / (k * cos_lat)
            self.__center_lat += delta.y() / k
            self.__press_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        if not self.__dragged:
            number = self.__space_at(event.position())
            if number is not None:
                self.space_clicked.emit(number)
        self.__press_pos = None

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def __space_at(self, position: QPointF) -> Optional[int]:
        for space in self.__spaces:
            center = self.__location_to_screen(space.location)
            if math.hypot(center.x() - position.x(), center.y() - position.y()) <= self.MARKER_RADIUS:
                return space.number
        return None

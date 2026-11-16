class ApplicationError(Exception):
    default_message = "Error"

    def __init__(self, message: str = ""):
        super().__init__(message or self.default_message)


class ValidationError(ApplicationError):
    default_message = "Неверные данные"


class UserNotFoundError(ApplicationError):
    default_message = "Пользователь не найден"


class SpaceNotFoundError(ApplicationError):
    default_message = "Парковочное место не найдено"


class SpaceUnavailableError(ApplicationError):
    default_message = "Парковочное место недоступно"


class ActiveBookingExistsError(ApplicationError):
    default_message = "У вас уже есть активная бронь"


class NoActiveBookingError(ApplicationError):
    default_message = "У вас нет активной брони"


class ActiveSessionExistsError(ApplicationError):
    default_message = "Вы уже занимаете парковочное место"


class NoActiveSessionError(ApplicationError):
    default_message = "У вас нет занятого парковочного места"


class InsufficientFundsError(ApplicationError):
    default_message = "Недостаточно средств в кошельке"
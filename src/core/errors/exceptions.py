from src.core.domain.user import User
from src.core.domain.weather import City


class DomainError(Exception):
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)


class CityNotFoundError(DomainError):
    def __init__(self, city: str):
        super().__init__(f'Данные для города c {city} отсутствуют в списке.')


class DatabaseError(DomainError):
    def __init__(self):
        super().__init__('Внутренняя ошибка, повторите попытку позже.')


class WeatherServiceAPIError(DomainError):
    def __init__(self):
        super().__init__('Внешний сервис погоды недоступен.')


class CityAlreadyExists(DomainError):
    def __init__(self, city: str):
        super().__init__(f'Город {city} уже добавлен в список.')

class CityIsEmpty(DomainError):
    def __init__(self):
        super().__init__(f'Поле названия города не может быть пустым')


class UserAlreadyExists(DomainError):
    def __init__(self):
        super().__init__(f'Пользователь уже существует.')

class UserStringIsEmpty(DomainError):
    def __init__(self):
        super().__init__(f'Строка не может быть пустой.')

class InvalidCredentials(DomainError):
    def __init__(self):
        super().__init__(f'Неверные данные.')


class WeatherServiceError(Exception):
    message: str
    error_code: str

class WeatherAPIUnavailableError(WeatherServiceError):
    def __init__(self, message: str = "Weather API unavailable"):
        super().__init__(message=message, error_code="API_UNAVAILABLE")


class WeatherAPINetworkError(WeatherServiceError):
    def __init__(self, message: str = "Network error"):
        super().__init__(message=message, error_code="NETWORK_ERROR")


class WeatherAPITimeoutError(WeatherServiceError):
    def __init__(self, message: str = "Request timeout"):
        super().__init__(message=message, error_code="TIMEOUT_ERROR")

class WeatherAPIInvalidResponseError(WeatherServiceError):
    def __init__(self, message: str = "Invalid response format"):
        super().__init__(message=message, error_code="INVALID_RESPONSE")


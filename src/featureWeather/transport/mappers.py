from src.core.domain.user import User
from src.core.domain.weather import City, WeatherInTime

from src.featureWeather.transport.schemas.request import (
    UserRegistrationRequest,
    CityCreateRequest,
    WeatherByCityAndTimeRequest
)

from src.featureWeather.transport.schemas.response import (
    CityCreateDTO,
    WeatherForecastDTO
)


def to_domain_user(dto: UserRegistrationRequest) -> User:
    return User(
        login=dto.username,
        password=dto.password
    )


def to_domain_city(dto: CityCreateRequest, user_id: int) -> City:
    return City(
        user_id=user_id,
        city=dto.city,
        latitude=dto.latitude,
        longitude=dto.longitude
    )


def to_city_dto(domain) -> CityCreateDTO:
    return CityCreateDTO(
        id=domain.id,
        city=domain.city,
        latitude=domain.latitude,
        longitude=domain.longitude,
    )


def to_domain_weather(dto: WeatherByCityAndTimeRequest, user_id: int):
    return WeatherInTime(
        city=dto.city,
        user_id=user_id,
        at_time=dto.time,
        fields=[p.value for p in dto.parameters]
    )


def to_weather_dto(domain) -> WeatherForecastDTO:
    return WeatherForecastDTO(
        city=domain.city,
        temperature=domain.temperature,
        humidity=domain.humidity,
        wind_speed=domain.wind_speed,
        precipitation=domain.precipitation
    )

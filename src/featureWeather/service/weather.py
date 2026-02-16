from datetime import datetime
import httpx
from abc import ABC, abstractmethod
from src.core.config import settings

from src.core.errors.exceptions import (
    WeatherAPINetworkError,
    WeatherAPITimeoutError,
    WeatherAPIUnavailableError,
    CityIsEmpty, InvalidCredentials
)

from ..repository.weather import IWeatherRepository
from src.core.domain.weather import (
    City,
    CityCreate,
    WeatherForecast,
    WeatherInTime,
    WeatherCurrent,
    ForecastsList
)


class IWeatherService(ABC):

    @abstractmethod
    async def add_city(self, data: City) -> CityCreate:
        pass

    @abstractmethod
    async def get_cities(self, user_id: int) -> list[CityCreate]:
        pass

    @abstractmethod
    async def get_forecast(self, data: WeatherInTime) -> WeatherForecast:
        pass

    @abstractmethod
    async def get_current_weather(self, latitude: float, longitude: float) -> WeatherCurrent:
        pass

    @abstractmethod
    async def refresh_all_forecasts(self):
        pass


class WeatherService(IWeatherService):
    BASE_URL = settings.BASE_URL

    def __init__(self, repo: IWeatherRepository):
        self.repo = repo

    async def _fetch_weather(self, latitude: float, longitude: float) -> dict:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "minutely_15": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
            "timezone": "auto",
            "forecast_days": 1
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.BASE_URL, params=params)

            if response.status_code != 200:
                raise WeatherAPIUnavailableError(
                    f"Weather API returned status {response.status_code}"
                )

            return response.json()["minutely_15"]

        except httpx.ConnectError:
            raise WeatherAPINetworkError("Cannot connect to weather service")
        except httpx.TimeoutException:
            raise WeatherAPITimeoutError("Weather service timeout")
        except httpx.HTTPError as e:
            raise WeatherAPIUnavailableError(f"HTTP error: {str(e)}")

    def _map_to_domain(self, raw: dict) -> list[ForecastsList]:
        forecasts: list[ForecastsList] = []

        for i in range(len(raw["time"])):
            forecasts.append(
                ForecastsList(
                    timestamp=datetime.fromisoformat(raw["time"][i]),
                    temperature=raw["temperature_2m"][i],
                    humidity=raw["relative_humidity_2m"][i],
                    wind_speed=raw["wind_speed_10m"][i],
                    precipitation=raw["precipitation"][i],
                )
            )

        return forecasts

    async def add_city(self, data: City) -> CityCreate:
        city = await self.repo.save_city(data)

        if data.city == "":
            raise CityIsEmpty()

        if data.latitude < -90 or data.latitude > 90 or data.longitude < -180 or data.longitude > 180:
            raise InvalidCredentials()

        raw = await self._fetch_weather(data.latitude, data.longitude)
        forecasts = self._map_to_domain(raw)

        await self.repo.replace_forecasts(city.id, forecasts)

        return city

    async def refresh_all_forecasts(self):
        try:
            cities = await self.repo.get_all_cities()

            for city in cities:
                raw = await self._fetch_weather(city.latitude, city.longitude)
                forecasts = self._map_to_domain(raw)

                await self.repo.replace_forecasts(city.id, forecasts)

        except httpx.ConnectError:
            raise WeatherAPINetworkError("Отсутствует подключение к интернету")
        except httpx.TimeoutException:
            raise WeatherAPITimeoutError("Таймаут сервиса")
        except httpx.HTTPError as e:
            raise WeatherAPIUnavailableError(f"Ошибка HTTP: {str(e)}")

    async def get_cities(self, user_id: int) -> list[CityCreate]:
        return await self.repo.get_users_cities(user_id)

    async def get_forecast(self, data: WeatherInTime) -> WeatherForecast:
        return await self.repo.get_forecast(data)

    async def get_current_weather(self, latitude: float, longitude: float) -> WeatherCurrent:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m,pressure_msl",
            "timezone": "auto",
        }

        if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
            raise InvalidCredentials()

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.BASE_URL, params=params)

            if response.status_code != 200:
                raise WeatherAPIUnavailableError(
                    f"Weather API returned status {response.status_code}"
                )

            data = response.json()["current"]

            return WeatherCurrent(
                temperature=data["temperature_2m"],
                wind_speed=data["wind_speed_10m"],
                pressure=data["pressure_msl"],
            )

        except httpx.ConnectError:
            raise WeatherAPINetworkError("Отсутствует подключение к интернету")
        except httpx.TimeoutException:
            raise WeatherAPITimeoutError("Таймаут сервиса")
        except httpx.HTTPError as e:
            raise WeatherAPIUnavailableError(f"Ошибка HTTP: {str(e)}")

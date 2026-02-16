from dataclasses import dataclass
from datetime import time, datetime
from typing import Optional


@dataclass
class City:
    user_id: int
    city: str
    latitude: float
    longitude: float


@dataclass
class WeatherInTime:
    city: str
    user_id: int
    at_time: time
    fields: list


@dataclass
class WeatherCurrent:
    temperature: float
    wind_speed: float
    pressure: float


@dataclass
class CityCreate:
    city: str
    latitude: float
    longitude: float
    id: int


@dataclass
class WeatherForecast:
    city: str
    temperature: Optional[float] = None
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    precipitation: Optional[float] = None


@dataclass
class ForecastsList:
    timestamp: datetime
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float

from pydantic import BaseModel, Field
from typing import List
from datetime import time
from enum import Enum


class WeatherParameter(str, Enum):
    """Параметры погоды для API"""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    PRECIPITATION = "precipitation"


class CoordinatesRequest(BaseModel):
    """DTO координат для запроса"""
    latitude: float
    longitude: float


class CityCreateRequest(CoordinatesRequest):
    """Запрос добавления города"""
    city: str = Field(..., max_length=50)


class WeatherByCityAndTimeRequest(BaseModel):
    """Запрос погоды на время"""
    city: str = Field(..., max_length=50)
    time: time
    parameters: List[WeatherParameter] = Field(
        default_factory=lambda: [WeatherParameter.TEMPERATURE]
    )


class UserRegistrationRequest(BaseModel):
    """Запрос регистрации пользователя"""
    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)
from pydantic import BaseModel, Field
from typing import List
from datetime import time
from enum import Enum


class WeatherParameter(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    PRECIPITATION = "precipitation"


class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float


class CityCreateRequest(CoordinatesRequest):
    city: str = Field(..., max_length=50)


class WeatherByCityAndTimeRequest(BaseModel):
    city: str = Field(..., max_length=50)
    time: time
    parameters: List[WeatherParameter] = Field(
        default_factory=lambda: [WeatherParameter.TEMPERATURE]
    )


class UserRegistrationRequest(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)

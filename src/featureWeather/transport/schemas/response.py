from typing import Optional
from pydantic import BaseModel


class WeatherUnitsDTO(BaseModel):
    time: str
    interval: str
    temperature_2m: str
    wind_speed_10m: str
    pressure_msl: str


class WeatherCurrentDTO(BaseModel):
    temperature: float
    wind_speed: float
    pressure: float


class CityDTO(BaseModel):
    id: int
    user_id: int
    city: str
    latitude: float
    longitude: float


class CityCreateDTO(BaseModel):
    city: str
    latitude: float
    longitude: float
    id: int

class WeatherForecastDTO(BaseModel):
    city: str
    temperature: Optional[float] = None
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    precipitation: Optional[float] = None


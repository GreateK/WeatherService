from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

from ..repository.user import UserRepository
from ..repository.weather import Weather
from ..service.user import AuthService
from ..service.weather import WeatherService


def get_user_repo(session: AsyncSession = Depends(get_db)):
    return UserRepository(session)


def get_weather_repo(session: AsyncSession = Depends(get_db)):
    return Weather(session)


def get_auth_service(repo: UserRepository = Depends(get_user_repo)):
    return AuthService(repo)


def get_weather_service(repo: Weather = Depends(get_weather_repo)):
    return WeatherService(repo)

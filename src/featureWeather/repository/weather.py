from abc import ABC, abstractmethod
from datetime import datetime, date, time

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.errors.exceptions import (
    CityAlreadyExists,
    DatabaseError,
    CityNotFoundError
)

from src.core.domain.weather import (
    City,
    WeatherInTime,
    CityCreate,
    WeatherForecast,
    ForecastsList
)
from .models import CitiesModel, ForecastsModel


class IWeatherRepository(ABC):
    @abstractmethod
    async def save_city(self, data: City) -> CityCreate:
        pass
    async def get_users_cities(self, user_id) -> list[CityCreate]:
        pass
    async def get_all_cities(self) -> list[CityCreate]:
        pass
    async def get_forecast(self, data: WeatherInTime) -> WeatherForecast:
        pass
    async def save_forecasts(self, city_id, forecasts: list[ForecastsList]):
        pass
    async def replace_forecasts(self, city_id: int, forecasts: list[ForecastsList]):
        pass


class Weather(IWeatherRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_city(self, data: City) -> CityCreate:
        try:
            stmt = select(CitiesModel).where(
                CitiesModel.name == data.city,
                CitiesModel.user_id == data.user_id
            )

            result = await self.session.execute(stmt)
            exists = result.scalar_one_or_none()

            if exists:
                raise CityAlreadyExists(city=data.city)

            model = CitiesModel(
                name=data.city,
                user_id=data.user_id,
                latitude=data.latitude,
                longitude=data.longitude
            )

            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

            return CityCreate(
                id=model.id,
                city=model.name,
                latitude=model.latitude,
                longitude=model.longitude
            )

        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


    async def get_users_cities(self, user_id) -> list[CityCreate]:
        try:
            query = (
                select(CitiesModel)
                .where(CitiesModel.user_id == user_id)
                .order_by(CitiesModel.name)
            )

            result = await self.session.execute(query)
            models = result.scalars().all()

            return [
                CityCreate(
                    id=m.id,
                    city=m.name,
                    latitude=m.latitude,
                    longitude=m.longitude,
                )
                for m in models
            ]

        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


    async def get_all_cities(self) -> list[CityCreate]:
        try:
            result = await self.session.execute(
                select(CitiesModel).order_by(CitiesModel.name)
            )

            models = result.scalars().all()

            return [
                CityCreate(
                    id=m.id,
                    city=m.name,
                    latitude=m.latitude,
                    longitude=m.longitude,
                )
                for m in models
            ]

        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


    async def get_forecast(self, data: WeatherInTime) -> WeatherForecast | None:
        try:
            stmt = select(CitiesModel).where(
                CitiesModel.name == data.city,
                CitiesModel.user_id == data.user_id
            )

            result = await self.session.execute(stmt)
            selected_city = result.scalar_one_or_none()

            if not selected_city:
                raise CityNotFoundError(city=data.city)

            minute = (data.at_time.minute // 15) * 15

            dt = datetime.combine(
                date.today(),
                time(data.at_time.hour, minute)
            )

            stmt = select(ForecastsModel).where(
                ForecastsModel.city_id == selected_city.id,
                ForecastsModel.timestamp == dt
            )

            result = await self.session.execute(stmt)

            forecast = result.scalar_one_or_none()

            if not forecast:
                return None

            return WeatherForecast(
                city=selected_city.name,
                temperature=forecast.temperature if "temperature" in data.fields else None,
                humidity=forecast.humidity if "humidity" in data.fields else None,
                wind_speed=forecast.wind_speed if "wind_speed" in data.fields else None,
                precipitation=forecast.precipitation if "precipitation" in data.fields else None,
            )

        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


    async def save_forecasts(self, city_id: int, forecasts: list[ForecastsList]):
        try:
            models = [
                ForecastsModel(
                    city_id=city_id,
                    timestamp=f.timestamp,
                    temperature=f.temperature,
                    humidity=f.humidity,
                    wind_speed=f.wind_speed,
                    precipitation=f.precipitation,
                )
                for f in forecasts
            ]

            self.session.add_all(models)
            await self.session.commit()

        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


    async def replace_forecasts(self, city_id: int, forecasts: list[ForecastsList]):
        try:
            await self.session.execute(
                delete(ForecastsModel).where(ForecastsModel.city_id == city_id)
            )
            models = [
                ForecastsModel(
                    city_id=city_id,
                    timestamp=f.timestamp,
                    temperature=f.temperature,
                    humidity=f.humidity,
                    wind_speed=f.wind_speed,
                    precipitation=f.precipitation,
                )
                for f in forecasts
            ]

            self.session.add_all(models)

            await self.session.commit()

        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


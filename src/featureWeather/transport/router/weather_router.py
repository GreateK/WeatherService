from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import List

from src.featureWeather.middleware.take_id_from_token import get_id_from_token

from src.featureWeather.transport.schemas.request import (
    CityCreateRequest,
    CoordinatesRequest,
    WeatherByCityAndTimeRequest
)

from src.featureWeather.transport.schemas.response import (
    CityCreateDTO,
    WeatherCurrentDTO,
    WeatherForecastDTO
)

from src.core.errors.exceptions import (
    CityIsEmpty,
    CityAlreadyExists,
    CityNotFoundError,
    WeatherAPIInvalidResponseError,
    WeatherAPINetworkError,
    WeatherAPITimeoutError,
    WeatherAPIUnavailableError,
    WeatherServiceError, InvalidCredentials
)

from src.featureWeather.service.weather import WeatherService
from src.featureWeather.transport.dependencies import get_weather_service
from src.featureWeather.transport.mappers import (
    to_domain_city,
    to_city_dto,
    to_domain_weather,
    to_weather_dto
)

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.post("/cities", response_model=CityCreateDTO)
async def add_city(
        req: Request,
        data: CityCreateRequest = ...,
        service: WeatherService = Depends(get_weather_service)
):
    user_id = get_id_from_token(req)

    try:
        domain = to_domain_city(data, user_id)
        result = await service.add_city(domain)
        return to_city_dto(result)

    except CityAlreadyExists as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "internal_error",
                "message": "Этот город уже добавлен в спсиок.",
                "details": str(e)
            }
        )
    except CityIsEmpty as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "internal_error",
                "message": "Поле названия города не может быть пустым.",
                "details": str(e)
            }
        )
    except InvalidCredentials as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "internal_error",
                "message": "Координаты неверны.",
                "details": str(e)
            }
        )


@router.get("/cities", response_model=List[CityCreateDTO])
async def get_cities(req: Request,
                     service: WeatherService = Depends(get_weather_service)
                     ):
    try:
        user_id = get_id_from_token(req)
        result = await service.get_cities(user_id)

        return [to_city_dto(c) for c in result]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "Неожиданная ошибка сервера.",
                "details": str(e)
            }
        )


@router.get("/forecast", response_model=WeatherForecastDTO | None)
async def forecast(req: Request,
                   data: WeatherByCityAndTimeRequest = Query(...),
                   service: WeatherService = Depends(get_weather_service)
                   ):
    user_id = get_id_from_token(req)

    try:
        domain = to_domain_weather(data, user_id)

        result = await service.get_forecast(domain)

        if not result:
            return None

        return to_weather_dto(result)

    except CityNotFoundError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "internal_error",
                "message": f"Город с названием {data.city} не найден",
                "details": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "Неожиданная ошибка сервера.",
                "details": str(e)
            }
        )


@router.get("/current", response_model=WeatherCurrentDTO)
async def get_current_weather(
        coords: CoordinatesRequest = Query(...),
        weather_service: WeatherService = Depends(get_weather_service)
):
    try:
        return await weather_service.get_current_weather(coords.latitude, coords.longitude)

    except InvalidCredentials as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "wrong_credentials",
                "message": "Введены неверные координаты.",
                "details": e.message
            }
        )
    except WeatherAPINetworkError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "network_error",
                "message": "Сетевая ошибка, проверьте интернет-соединение.",
                "details": e.message
            }
        )
    except WeatherAPITimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail={
                "error": "timeout_error",
                "message": "Сервис погоды не доступен, повторите попытку позже.",
                "details": e.message
            }
        )
    except WeatherAPIUnavailableError as e:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "service_unavailable",
                "message": "Сервис погоды временно недоступен.",
                "details": e.message
            }
        )
    except WeatherAPIInvalidResponseError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "invalid_response",
                "message": "Ошибка обработки данных от сервиса погоды.",
                "details": e.message
            }
        )
    except WeatherServiceError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": e.error_code,
                "message": "Внутренняя ошибка сервиса погоды.",
                "details": e.message
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "Неожиданная ошибка сервера.",
                "details": str(e)
            }
        )

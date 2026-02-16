import asyncio

from fastapi import FastAPI

from pathlib import Path

from src.database import setup_database
from src.database.database import AsyncSessionLocal
from src.featureWeather.repository.weather import Weather
from src.featureWeather.service.weather import WeatherService
from src.featureWeather.transport.router.auth_router import router as auth_router
from src.featureWeather.transport.router.weather_router import router as weather_router

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI(title="Weather REST API")

app.include_router(auth_router)
app.include_router(weather_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=415,
        content={"detail": "Недопустимый формат данных."}
    )


@app.on_event("startup")
async def startup():
    db_file = Path("weather.db")

    if not db_file.exists():
        print("База данных не найдена. Создаём...")
        await setup_database()
        print("База данных создана")

    async def weather_job():
        while True:
            try:
                async with AsyncSessionLocal() as session:
                    repo = Weather(session)
                    service = WeatherService(repo)

                    await service.refresh_all_forecasts()

                print("Forecasts updated")

            except Exception as e:
                print("Scheduler error:", e)

            await asyncio.sleep(900)

    asyncio.create_task(weather_job())


@app.get("/")
def root():
    return {"status": "ok"}

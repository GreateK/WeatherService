from fastapi import APIRouter, Depends, Response, HTTPException
from starlette import status

from src.featureWeather.transport.schemas.request import UserRegistrationRequest

from src.core.errors.exceptions import UserAlreadyExists, InvalidCredentials, UserStringIsEmpty

from src.featureWeather.service.user import AuthService
from src.featureWeather.transport.dependencies import get_auth_service
from src.featureWeather.transport.mappers import to_domain_user


router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- REGISTER ----------------

@router.post("/register")
async def register(
    data: UserRegistrationRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        domain_user = to_domain_user(data)
        created = await service.register(domain_user)

        return {
            "id": created.id,
            "login": created.login
        }

    except UserAlreadyExists:
        raise HTTPException(400, "Имя пользователя уже занято!")
    except UserStringIsEmpty:
        raise HTTPException(400, "Строка не может быть пустой!")
    except InvalidCredentials:
        raise HTTPException(400, f"Невалидные данные: логин минимум 4 символа, пароль должен содержать спецсимволы и заглавную букву.")


# ---------------- LOGIN ----------------

@router.post("/login")
async def login(
    data: UserRegistrationRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service)
):
    try:
        domain_user = to_domain_user(data)

        token, _ = await service.login(domain_user)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax"
        )

        return {"message": "Logged in"}

    except InvalidCredentials:
        raise HTTPException(401, "Неверные данные")


# ---------------- LOGOUT ----------------

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

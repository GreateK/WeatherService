from abc import ABC, abstractmethod

from ..repository.user import IUserRepository
from src.core.domain.user import User, UserCreated
from src.core.errors.exceptions import UserAlreadyExists, InvalidCredentials, UserStringIsEmpty, DatabaseError
from .security_service import hash_password, verify_password, create_access_token


class IAuthService(ABC):
    @abstractmethod
    async def register(self, user: User) -> UserCreated:
        pass

    async def login(self, user: User) -> UserCreated:
        pass


class AuthService(IAuthService):

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def register(self, user: User) -> UserCreated:
        try:
            exists = await self.repo.get_by_login(user.login)

            if exists:
                raise UserAlreadyExists()

            if user.login == "" or user.password == "":
                raise UserStringIsEmpty()

            user = UserCreated(
                id=None,
                login=user.login,
                password_hash=hash_password(user.password)
            )

            return await self.repo.create(user)
        except DatabaseError:
            raise InvalidCredentials()

    async def login(self, user: User) -> tuple[str, UserCreated]:
        user_created = await self.repo.get_by_login(user.login)

        if not user_created or not verify_password(user.password, user_created.password_hash):
            raise InvalidCredentials()

        token = create_access_token({"user_id": user_created.id})

        return token, user_created

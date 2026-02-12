from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import UserModel
from src.core.domain.user import User, UserCreated
from ...core.errors.exceptions import DatabaseError


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_login(self, login: str) -> UserCreated:
        pass
    async def create(self, user: UserCreated) -> UserCreated:
        pass


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_login(self, login: str) -> UserCreated | None:
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.login == login)
            )
            model = result.scalar_one_or_none()

            if not model:
                return None

            return UserCreated(
                id=model.id,
                login=model.login,
                password_hash=model.password_hash
            )
        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()

    async def create(self, user: UserCreated) -> UserCreated:
        try:
            model = UserModel(
                login=user.login,
                password_hash=user.password_hash
            )

            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

            return UserCreated(
                id=model.id,
                login=model.login,
                password_hash=model.password_hash
            )
        except SQLAlchemyError:
            await self.session.rollback()
            raise DatabaseError()


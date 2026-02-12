from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, CheckConstraint

from src.database import Base

class UserModel(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint("length(login) >= 4", name="login_min_length"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str]

    cities: Mapped[list["CitiesModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

class CitiesModel(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    latitude: Mapped[float]
    longitude: Mapped[float]

    user: Mapped["UserModel"] = relationship(back_populates="cities")

    forecasts: Mapped[list["ForecastsModel"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )


class ForecastsModel(Base):
    __tablename__ = 'forecasts'

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    temperature: Mapped[float]
    humidity: Mapped[float]
    precipitation: Mapped[float]
    wind_speed: Mapped[float]


    city: Mapped["CitiesModel"] = relationship(back_populates="forecasts")


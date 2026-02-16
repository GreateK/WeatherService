from dataclasses import dataclass


@dataclass
class User:
    login: str
    password: str


@dataclass
class UserCreated:
    id: int | None
    login: str
    password_hash: str

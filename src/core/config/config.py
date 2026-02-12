import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        # База данных
        self.DATABASE_URL = self._get_value("DATABASE_URL")
        self.BASE_URL = self._get_value("BASE_URL")

        # JWT
        self.SECRET_KEY = self._get_value("SECRET_KEY")
        self.ALGORITHM = self._get_env("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = self._get_alive("ACCESS_TOKEN_EXPIRE_MINUTES")

    def _get_env(self, key, default="HS256"):
        value = os.getenv(key)
        if value is None:
            return default
        return value

    def _get_value(self, key):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"В .env файле не обнаружено: {key}")
        return value

    def _get_alive(self, key, default: int = 60):
        value = os.getenv(key)
        if not value:
            return default

        try:
            return int(value)
        except ValueError:
            print(f"Ошибка: {key} должен быть числом, используется {default}")
            return default


try:
    settings = Config()
    print("Конфигурация загружена успешно")
except ValueError as e:
    print(f"Ошибка загрузки конфигурации: {e}")
    exit(1)

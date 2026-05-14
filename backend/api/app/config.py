from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# app/config.py -> app/; la raíz del proyecto está un nivel por encima
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_PATH = BASE_DIR / "data" / "administradora.db"


class Settings(BaseSettings):
    # SQLite: por defecto usa data/administradora.db
    database_path: Path = DEFAULT_DATABASE_PATH
    jwt_secret_key: str = "cambia-esta-clave-en-produccion"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480
    angular_origins: str = "http://localhost:4200,http://127.0.0.1:4200"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def angular_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.angular_origins.split(",") if origin.strip()]


settings = Settings()

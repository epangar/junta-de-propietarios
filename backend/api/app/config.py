from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str = "cambia_esta_clave_en_produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    db_path: str = "data/administradora.db"
    angular_origins: str = "http://localhost:4200,http://127.0.0.1:4200"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    @property
    def database_path(self) -> Path:
        raw = Path(self.db_path)
        return raw if raw.is_absolute() else self.base_dir / raw

    @property
    def angular_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.angular_origins.split(",") if origin.strip()]

settings = Settings()

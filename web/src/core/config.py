from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path


class Settings(BaseSettings):
    ENV_TYPE: str

    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    MODE: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    default_day_work_hours: int = 4
    default_task_work_hours: int = 2
    default_interest: int = 5
    default_importance: int = 5

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=Path(__file__).parents[3] / ".env", env_ignore_missing=True)


settings = Settings()


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

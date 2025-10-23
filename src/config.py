from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    VERSION: str
    PROJECT_NAME: str
    API_V1_STR: str
    ALL_CORS_ORIGINS: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SQLALCHEMY_DATABASE_URI: str
    DATABASE_ENGINE_POOL_TIMEOUT: int
    DATABASE_ENGINE_POOL_RECYCLE: int
    DATABASE_ENGINE_POOL_SIZE: int
    DATABASE_ENGINE_MAX_OVERFLOW: int
    DATABASE_ENGINE_POOL_PING: bool

    model_config = SettingsConfigDict(env_file="/local/projects/home-budget-app/src/.env")

#settings = Settings(_env_file="D:/dev/devot-api/src/test.env")
settings = Settings()

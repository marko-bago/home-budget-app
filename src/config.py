from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    VERSION: str
    PROJECT_NAME: str
    API_V1_STR: str
    ALL_CORS_ORIGINS: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TEST_DATABASE_URL: str
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_ENGINE_POOL_TIMEOUT: int
    DATABASE_ENGINE_POOL_RECYCLE: int
    DATABASE_ENGINE_POOL_SIZE: int
    DATABASE_ENGINE_MAX_OVERFLOW: int
    DATABASE_ENGINE_POOL_PING: bool

    DEFAULT_CATEGORIES: list[dict] = [
        {"name": "Groceries", "description": "Money spent at grocery shops"},
        {"name": "Transport", "description": "Gas, public transit, and ride shares"},
        {"name": "Housing", "description": "Rent/Mortgage and utilities"},
        {"name": "Dining", "description": "Restaurants, street food, ordering take-out"},
        {"name": "Drinks", "description": "Going out for coffee, alcohol or other drinks"},
        {"name": "Clothing", "description": "Clothes, shoes, fashion accessories"},
        {"name": "Education", "description": "Education cost, seminars, webinars, courses"},
        {"name": "Electronics", "description": "Machines, gadgets, tools, computers..."},
        {"name": "Subscriptions", "description": "Netflix, Spotify, Youtube and so on"},
        {"name": "Health", "description": "Doctor bills"},
        {"name": "Leisure", "description": "Movies, Museums, Festivals..."},
        {"name": "Payment", "description": "Payment to account"}, # for income
        {"name": "Other", "description": "Everything else"},
    ]

    model_config = SettingsConfigDict(env_file=".env")

#settings = Settings(_env_file="test.env")
settings = Settings()

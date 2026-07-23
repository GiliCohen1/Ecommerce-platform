from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    redis_url: str = "redis://localhost:6379"
    # Comma-separated list of allowed CORS origins.
    # In Vercel, set this to your frontend URL, e.g. https://my-shop.vercel.app
    allowed_origins: str = "http://localhost:8081,http://127.0.0.1:8081"


settings = Settings()

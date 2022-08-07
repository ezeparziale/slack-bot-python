from pydantic import BaseSettings


class Settings(BaseSettings):
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str
    WEATHER_TOKEN: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str
    WEATHER_TOKEN: str
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = ".env"


settings = Settings()

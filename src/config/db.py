from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    DB_CONNECTION_STR: str
    RENT_APARTMENTS_TABLE_NAME: str


db_settings = DBSettings()

engine = create_engine(db_settings.DB_CONNECTION_STR)

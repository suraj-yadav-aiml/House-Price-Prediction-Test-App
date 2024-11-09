import ast

from loguru import logger
from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8"
    )

    COLUMNS_TO_ENCODE: str  # Store as a string initially
    COLUMNS_X: str          # Store as a string initially
    COLUMNS_Y: str
    TEST_SIZE: float
    CV: int
    SCORING: str
    GRID_SPACE: str         # Store as a string initially
    MODEL_PATH: DirectoryPath
    MODEL_NAME: str
    LOG_LEVEL: str
    DB_CONNECTION_STR: str
    RENT_APARTMENTS_TABLE_NAME: str

    # Custom initialization to parse string fields after loading
    def __post_init__(self):
        self.COLUMNS_TO_ENCODE = ast.literal_eval(self.COLUMNS_TO_ENCODE)
        self.COLUMNS_X = ast.literal_eval(self.COLUMNS_X)
        self.GRID_SPACE = ast.literal_eval(self.GRID_SPACE)


def configure_logging(log_level: str) -> None:

    # logger.remove()  # remove logs from console
    logger.add(
        "logs/app.log",
        rotation="1 day",
        retention="2 days",
        compression="zip",
        level=log_level
    )


settings = Settings()
configure_logging(log_level=settings.LOG_LEVEL)


engine = create_engine(settings.DB_CONNECTION_STR)

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    LOG_LEVEL: str


def configure_logging(log_level: str, output_to_console=True) -> None:

    if not output_to_console:
        logger.remove()  # remove logs from console

    logger.add(
        "logs/app.log",
        rotation="1 day",
        retention="2 days",
        compression="zip",
        level=log_level
    )


configure_logging(log_level=LoggerSettings().LOG_LEVEL,
                  output_to_console=True)




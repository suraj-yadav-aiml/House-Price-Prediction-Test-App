import ast

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8",
        extra="ignore"
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

    # Custom initialization to parse string fields after loading
    def __post_init__(self):
        self.COLUMNS_TO_ENCODE = ast.literal_eval(self.COLUMNS_TO_ENCODE)
        self.COLUMNS_X = ast.literal_eval(self.COLUMNS_X)
        self.GRID_SPACE = ast.literal_eval(self.GRID_SPACE)


model_settings = ModelSettings()


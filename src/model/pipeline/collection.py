import os
from typing import Optional

from loguru import logger
import pandas as pd
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from config import engine
from db.db_model import RentApartments


def load_data(path: str) -> Optional[pd.DataFrame]:
    """
    Loads data from a CSV file into a pandas DataFrame.

    Args:
        path (str): The file path to the CSV file. Defaults to 'rent_apartments.csv'.

    Returns:
        Optional[pd.DataFrame]: A pandas DataFrame containing the loaded data, or None if the file does not exist.

    Raises:
        ValueError: If the file is not found or is not a CSV file.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file contains parsing errors.

    Example:
        >>> df = load_data("data.csv")
        >>> if df is not None:
        >>>     print(df.head())
    """

    logger.info(f"Loading CSV file from {path}")

    # Check if file exists
    if not os.path.exists(path):
        logger.error(f"The file '{path}' does not exist.")
        raise ValueError(f"The file '{path}' does not exist.")
    # Check if the file has a .csv extension
    if not path.endswith('.csv'):
        logger.error("The file must be a CSV (.csv) file.")
        raise ValueError("The file must be a CSV (.csv) file.")
    try:
        # Load the CSV file into a pandas DataFrame
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        logger.error(f"Error: The file '{path}' is empty.")
        return None
    except pd.errors.ParserError as e:
        logger.error(f"Error: There was an issue parsing the file '{path}'. Details: {e}")
        return None


def load_data_from_db() -> pd.DataFrame:
    """
    Extracts data from the RentApartments table in the database and returns it
    as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the table data.   
    Raises:
        ValueError: If data extraction fails due to a SQLAlchemyError.
    """
    logger.info("Extracting table from the database...")

    try:
        query = select(RentApartments)
        data = pd.read_sql(
            query,
            engine
        )
        logger.info("Data extraction successful.")
        return data
    except SQLAlchemyError as e:
        logger.error("Failed to load data from the database: {}", e)
        raise ValueError("Could not load data from the database.") from e


if __name__ == "__main__":

    # df = load_data(settings.DATA_FILE_NAME)
    # if df is not None:
    #     print(df.head())
    # else:
    #     print("Failed to load data.")
    data = load_data_from_db()
    print(data.head())

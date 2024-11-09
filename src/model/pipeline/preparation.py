import ast
import re
from typing import Optional

import pandas as pd
from loguru import logger

from config.constants import settings
from model.pipeline.collection import load_data_from_db


def encode_cat_cols(
        data: pd.DataFrame,
        columns: Optional[list] = None
) -> pd.DataFrame:
    """
    Encodes categorical columns into dummy/indicator variables.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be encoded.
        columns (Optional[list]): List of categorical columns to encode.                         

    Returns:
        pd.DataFrame: DataFrame with categorical columns encoded as dummy variables.

    Raises:
        ValueError: If any column in `columns` is not found in the DataFrame.
    """
    # Ensure all specified columns are in the DataFrame
    missing_cols = [col for col in columns if col not in data.columns]
    if missing_cols:
        logger.warning(f"The following columns are not found in the DataFrame: {', '.join(missing_cols)}")
        raise ValueError(f"The following columns are not found in the DataFrame: {', '.join(missing_cols)}")
    # Encode categorical columns with dummy variables
    logger.info(f"Encoding categorical columns : {columns}")
    return pd.get_dummies(data, columns=columns, drop_first=True)


def parse_garden_col(data: pd.DataFrame) -> pd.DataFrame:
    """
    Parses the 'garden' column to convert categorical values into numerical
    values.

    Args:
        data (pd.DataFrame): The DataFrame containing the 'garden' column to
                             be parsed.

    Returns:
        pd.DataFrame: DataFrame with the 'garden' column parsed into numerical
                      values.

    Raises:
        ValueError: If the 'garden' column is not found in the DataFrame.
    """
    if 'garden' not in data.columns:
        logger.error("The 'garden' column is not found in the DataFrame.")
        raise ValueError("The 'garden' column is not found in the DataFrame.")

    def parse_garden_value(value: str) -> int:
        if value == 'Not present':
            return 0
        else:
            # Extract the first number from the string using regex
            match = re.search(r'\d+', value)
            return int(match.group(0)) if match else 0

    # Apply the parsing function to the 'garden' column
    logger.info("Parsing 'garden' column")
    data['garden'] = data['garden'].apply(parse_garden_value)

    return data


def prepare_data() -> Optional[pd.DataFrame]:
    """
    Prepares the rental apartment data by loading, encoding, and parsing
    columns.

    Args:
        path (str): The file path to the CSV file. Defaults to
                    'rent_apartments.csv'.

    Returns:
        Optional[pd.DataFrame]: The cleaned and prepared DataFrame
                                or None if loading fails.

    Raises:
        ValueError: If the CSV file cannot be loaded.
    """

    logger.info("Starting pre-processing pipeline")

    # Load the data
    # data = load_data(path)
    data = load_data_from_db()

    if data is None:
        return None

    # Encode categorical columns
    encoded_data = encode_cat_cols(data, ast.literal_eval(settings.COLUMNS_TO_ENCODE))

    # Parse 'garden' column
    df = parse_garden_col(encoded_data)

    return df


if __name__ == "__main__":

    df = prepare_data(settings.DATA_FILE_NAME)

    if df is not None:
        print(df['garden'])
    else:
        print("Failed to load and prepare data.")

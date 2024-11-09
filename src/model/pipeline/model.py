from model.pipeline.preparation import prepare_data
import ast
import os
import pickle as pk
from typing import Tuple

import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

from config import model_settings  # COLUMNS_X, COLUMNS_Y, TEST_SIZE, CV, SCORING, GRID_SPACE, MODEL_SAVE_PATH


def build_model() -> None:
    """
    Main function to build, evaluate, and save the model.

    Steps:
        1. Prepares the data by extracting feature (X) and
           target (y) variables.
        2. Splits the data into training and testing sets.
        3. Trains the RandomForestRegressor model using GridSearchCV.
        4. Evaluates the model on the test set.
        5. Saves the trained model to the specified path.

    Raises:
        ValueError: If data preparation fails or any key constant is missing.
        Exception: If model training or saving encounters issues.
    """
    try:
        logger.info("Starting the model building pipeline")
        # Step 1: Prepare data
        df = prepare_data()
        if df is None or df.empty:
            logger.warning("Data loading failed.",
                           "Please ensure the data is available and correctly formatted.")
            raise ValueError("Data loading failed.",
                             "Please ensure the data is available and correctly formatted.")

        # Step 2: Extract X (features) and y (target)
        X, y = get_X_y(df, ast.literal_eval(model_settings.COLUMNS_X), model_settings.COLUMNS_Y)

        # Step 3: Train-test split
        logger.info("Split data into train and test")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=model_settings.TEST_SIZE, random_state=42)

        # Step 4: Train the model
        model = train_model(
            X_train,
            y_train
        )

        # Step 5: Evaluate the model
        evaluate_model(
            model,
            X_test,
            y_test
        )

        # Step 6: Save the model
        save_model(
            model,
            f"{model_settings.MODEL_PATH}/{model_settings.MODEL_NAME}"
        ) 
    except ValueError as e:
        logger.error(f"ValueError: {e}")
    except Exception as e:
        logger.error(f"An error occurred during model building: {e}")


def get_X_y(data: pd.DataFrame, columns_X: list, column_y: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Extracts the features (X) and target (y) from the dataset.

    Args:
        data (pd.DataFrame): The full dataset.
        columns_X (list): List of feature columns to be used for X.
        column_y (str): The target column for y.

    Returns:
        Tuple[pd.DataFrame, pd.Series]: X (features) and y (target).

    Raises:
        KeyError: If specified columns are not found in the DataFrame.
    """
    logger.info("Get X and y")
    try:
        X = data[columns_X]
        y = data[column_y]
        return X, y
    except KeyError as e:
        raise KeyError(f"One or more specified columns are missing from the dataset: {e}")


def train_model(
        X_train: pd.DataFrame,
        y_train: pd.Series
) -> RandomForestRegressor:
    """
    Trains a RandomForestRegressor model using GridSearchCV to find the best parameters.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target.

    Returns:
        RandomForestRegressor: The best estimator found by GridSearchCV.

    Raises:
        Exception: If the model training encounters an issue.
    """
    logger.info("Training model with Hyperparameter tinning.")

    try:
        grid = GridSearchCV(RandomForestRegressor(),
                            param_grid=ast.literal_eval(model_settings.GRID_SPACE),
                            cv=model_settings.CV,
                            scoring=model_settings.SCORING,
                            n_jobs=-1)

        grid.fit(X_train, y_train)
        return grid.best_estimator_
    except Exception as e:
        raise Exception(f"Error occurred during model training: {e}")


def evaluate_model(
        model: RandomForestRegressor,
        X_test: pd.DataFrame,
        y_test: pd.Series
) -> float:
    """
    Evaluates the model performance on the test dataset.

    Args:
        model (RandomForestRegressor): The trained model.
        X_test (pd.DataFrame): Testing features.
        y_test (pd.Series): Testing target.

    Returns:
        float: The model's score on the test set.
    """
    logger.info(f"Evaluating the model\n Score: {model.score(X_test, y_test)}")
    return model.score(X_test, y_test)


def save_model(
        model: RandomForestRegressor,
        file_name: str
) -> None:
    """
    Saves the trained model to a file using pickle.

    Args:
        model (RandomForestRegressor): The model to be saved.
        file_name (str): The path where the model should be saved.

    Raises:
        Exception: If saving the model encounters an issue.
    """
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'wb') as f:
            pk.dump(model, f)
        logger.info(f"Model successfully saved to {file_name}")
    except Exception as e:
        logger.error(f"Error occurred while saving the model: {e}")
        raise Exception(f"Error occurred while saving the model: {e}")


if __name__ == "__main__":

    build_model()

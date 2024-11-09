import pickle as pk
from pathlib import Path
from typing import List, Any

from loguru import logger

from config import model_settings
from model.pipeline.model import build_model


class ModelService:
    """
    A service class for loading a machine learning model and making
    predictions.

    Attributes:
        model: The machine learning model loaded from a file.
    """

    def __init__(self) -> None:
        """
        Initializes the ModelService instance with the model attribute set to
        None.
        """
        self.model = None

    def load_model(self, model_name: str) -> None:
        """
        Loads a machine learning model from a pickle file. If the model file
        doesn't exist, the model is built and saved.

        Args:
            model_name (str): The name of the model file to load
            (without extension).
        Raises:
            FileNotFoundError: If the model file is not found and cannot be
            built.
            Exception: If there's an issue with loading or building the model.
        """
        model_path = Path(f"{model_settings.MODEL_PATH}/{model_name}")

        try:
            if not model_path.exists():
                logger.info(f"Model file {model_name} not found.")
                logger.info("Again building the model...")
                build_model()
                if not model_path.exists():
                    logger.crirical(f"Model {model_name} could not be built or found.")
                    raise FileNotFoundError(f"Model {model_name} could not be built or found.")
            with open(model_path, 'rb') as f:
                self.model = pk.load(f)
            logger.info(f"Model {model_name} loaded successfully.")

        except FileNotFoundError as e:
            logger.error(f"FileNotFoundError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while loading the model: {e}")

    def predict(self, input_data: List[Any]) -> List[Any]:
        """
        Makes a prediction using the loaded model.

        Args:
            input_data (List[Any]): A list of input features for prediction.
        Returns:
            List[Any]: The predicted output as a list of values.
        Raises:
            ValueError: If the model is not loaded.
            Exception: If there's an issue during prediction.
        """
        try:
            if self.model is None:
                logger.error("Model is not loaded. Please load a model first.")
                raise ValueError("Model is not loaded. Please load a model first.")
            logger.info("Making Prediction")
            prediction = self.model.predict([input_data])
            return prediction.tolist()

        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            return []


if __name__ == "__main__":

    ms = ModelService()
    ms.load_model(model_settings.MODEL_NAME)

    input_data = [85, 2015, 2, 20, 1, 1, 0, 0, 1]
    prediction = ms.predict(input_data)
    print(f"Prediction for input {input_data}: {prediction}")

import warnings

from loguru import logger

from config.constants import settings
from model.model_service import ModelService


warnings.filterwarnings("ignore")

@logger.catch
def main():
    logger.info("Running the application...")
    ms = ModelService()
    ms.load_model(settings.MODEL_NAME)

    feature_values = {
        'area': 85,
        'constraction_year': 2015,
        'bedrooms': 2,
        'garden_area': 20,
        'balcony_present': 1,
        'parking_present': 1,
        'furnished': 0,
        'garage_present': 0,
        'storage_present': 1,
    }

    prediction = ms.predict(list(feature_values.values()))
    logger.info(f"Prediction for input {feature_values.values()}: {prediction}")


if __name__ == "__main__":
    main()

# collection.py, preparation.py, model.py, model_service.py, runner.py

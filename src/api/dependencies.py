
# src/api/dependencies.py
from functools import lru_cache
from src.services.prediction_service import PredictionService
import logging

logger = logging.getLogger(__name__)

@lru_cache()
def get_prediction_service() -> PredictionService:
    """
    Retourne une instance singleton du service de prédiction
    """
    try:
        return PredictionService()
    except Exception as e:
        logger.error(f"Erreur lors de la création du service de prédiction: {e}")
        raise


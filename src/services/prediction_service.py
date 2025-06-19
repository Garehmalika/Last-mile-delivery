import pickle
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from ..api.schemas.prediction import PickupFeatures, DeliveryFeatures
from ..utils.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ModelManager:
    def __init__(self):
        self.model_pickup = None
        self.model_delivery = None
        self.pickup_feature_names = None
        self.delivery_feature_names = None
        self.model_load_time = None
        self._load_models()

    def _load_models(self):
        """Charge les modèles pickle"""
        self.model_load_time = datetime.now()
        
        # Chargement du modèle pickup
        pickup_path = Path(settings.PICKUP_MODEL_PATH)
        if pickup_path.exists():
            try:
                with open(pickup_path, 'rb') as f:
                    self.model_pickup = pickle.load(f)
                logger.info(f"Modèle pickup chargé avec succès depuis {pickup_path}")
            except Exception as e:
                logger.error(f"Erreur chargement {pickup_path} : {e}")
        else:
            logger.warning(f"Fichier {pickup_path} introuvable")

        # Chargement du modèle delivery
        delivery_path = Path(settings.DELIVERY_MODEL_PATH)
        if delivery_path.exists():
            try:
                with open(delivery_path, 'rb') as f:
                    self.model_delivery = pickle.load(f)
                logger.info(f"Modèle delivery chargé avec succès depuis {delivery_path}")
            except Exception as e:
                logger.error(f"Erreur chargement {delivery_path} : {e}")
        else:
            logger.warning(f"Fichier {delivery_path} introuvable")

        # Définition des noms de features pour delivery
        self.delivery_feature_names = [
            'courier_id', 'lng', 'lat', 'aoi_id',
            'accept_time_seconds', 'accept_gps_time_seconds', 'accept_gps_lng', 'accept_gps_lat',
            'delivery_time_seconds', 'delivery_gps_time_seconds', 'delivery_gps_lng', 'delivery_gps_lat',
            'delivery_time_minutes', 'accept_hour', 'accept_day', 'city_encoded', 'distance',
            'day_of_week', 'hour_of_day', 'task_duration_seconds', 'log_task_duration',
            'delivery_hour', 'delivery_weekday', 'task_duration_seconds_conv'
        ]

    def predict_pickup(self, features: PickupFeatures) -> Dict[str, Any]:
        """Prédiction pour pickup avec métadonnées"""
        if self.model_pickup is None:
            raise ValueError("Modèle pickup non disponible")

        try:
            input_data = features.to_model_input()
            feature_names = list(input_data.keys())
            input_df = pd.DataFrame([list(input_data.values())], columns=feature_names)
            
            prediction = self.model_pickup.predict(input_df)
            prediction_value = float(prediction[0])
            
            # Calcul du score de confiance basique
            confidence_score = self._calculate_confidence_score(
                prediction_value, 
                features.waiting_time_minutes
            )
            
            return {
                "prediction": prediction_value,
                "confidence_score": confidence_score,
                "model_version": "lasso_pickup_v1.0",
                "features_count": len(input_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur prédiction pickup : {e}")
            raise ValueError(f"Erreur prédiction pickup : {str(e)}")

    def predict_delivery(self, features: DeliveryFeatures) -> Dict[str, Any]:
        """Prédiction pour delivery avec métadonnées"""
        if self.model_delivery is None:
            raise ValueError("Modèle delivery non disponible")

        try:
            feature_array = features.to_feature_array()
            input_df = pd.DataFrame([feature_array], columns=self.delivery_feature_names)
            
            # Vérifier si le modèle a un attribut feature_names_in_
            if hasattr(self.model_delivery, 'feature_names_in_'):
                model_features = list(self.model_delivery.feature_names_in_)
                input_df = input_df.reindex(columns=model_features, fill_value=0)
            
            prediction = self.model_delivery.predict(input_df)
            prediction_value = float(prediction[0])
            
            # Calcul du score de confiance
            confidence_score = self._calculate_confidence_score(
                prediction_value, 
                features.distance
            )
            
            return {
                "prediction": prediction_value,
                "confidence_score": confidence_score,
                "model_version": "lasso_delivery_v1.0",
                "features_count": len(feature_array)
            }
            
        except Exception as e:
            logger.error(f"Erreur prédiction delivery : {e}")
            if hasattr(self.model_delivery, 'feature_names_in_'):
                logger.error(f"Features attendues: {list(self.model_delivery.feature_names_in_)}")
            raise ValueError(f"Erreur prédiction delivery : {str(e)}")

    def _calculate_confidence_score(self, prediction: float, reference_value: float) -> float:
        """Calcule un score de confiance basique"""
        # Score de confiance basé sur la cohérence de la prédiction
        if prediction < 0:
            return 0.1  # Très faible confiance pour prédictions négatives
        elif prediction < 30:  # Prédictions courtes
            return 0.9
        elif prediction < 60:  # Prédictions moyennes
            return 0.7
        else:  # Prédictions longues
            return 0.5

    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les informations sur les modèles chargés"""
        return {
            "pickup_model": {
                "loaded": self.is_pickup_available(),
                "type": "Lasso Regression" if self.model_pickup else None,
                "features_count": len(self.pickup_feature_names) if self.pickup_feature_names else 0
            },
            "delivery_model": {
                "loaded": self.is_delivery_available(),
                "type": "Lasso Regression" if self.model_delivery else None,
                "features_count": len(self.delivery_feature_names) if self.delivery_feature_names else 0
            },
            "load_time": self.model_load_time.isoformat() if self.model_load_time else None
        }

    def get_uptime(self) -> Optional[float]:
        """Retourne le temps de fonctionnement en secondes"""
        if self.model_load_time:
            return (datetime.now() - self.model_load_time).total_seconds()
        return None

    def is_pickup_available(self) -> bool:
        return self.model_pickup is not None

    def is_delivery_available(self) -> bool:
        return self.model_delivery is not None

    def reload_models(self):
        """Recharge les modèles (utile pour les mises à jour)"""
        logger.info("Rechargement des modèles...")
        self._load_models()
        logger.info("Rechargement terminé")


# Instance globale du gestionnaire de modèles
model_manager = ModelManager()
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Valeur prédite en minutes")
    model_version: str = Field(..., description="Version du modèle utilisé")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la prédiction")
    confidence_score: Optional[float] = Field(None, description="Score de confiance de la prédiction")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Statut de l'API")
    pickup_model_loaded: bool = Field(..., description="Modèle pickup chargé")
    delivery_model_loaded: bool = Field(..., description="Modèle delivery chargé")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp du check")
    uptime_seconds: Optional[float] = Field(None, description="Temps de fonctionnement en secondes")


class ValidationResponse(BaseModel):
    status: str = Field(..., description="Statut de validation")
    message: str = Field(..., description="Message descriptif")
    processed_features: int = Field(..., description="Nombre de features traitées")
    feature_summary: Optional[Dict[str, Any]] = Field(None, description="Résumé des features")
    warnings: Optional[list] = Field(None, description="Avertissements éventuels")


class ModelStatusResponse(BaseModel):
    pickup_model: Dict[str, Any] = Field(..., description="Statut du modèle pickup")
    delivery_model: Dict[str, Any] = Field(..., description="Statut du modèle delivery")
    last_updated: datetime = Field(default_factory=datetime.now, description="Dernière mise à jour")


class DebugResponse(BaseModel):
    api_features: list = Field(..., description="Features utilisées par l'API")
    api_feature_count: int = Field(..., description="Nombre de features API")
    model_features: Optional[list] = Field(None, description="Features attendues par le modèle")
    model_feature_count: Optional[int] = Field(None, description="Nombre de features du modèle")
    features_match: Optional[bool] = Field(None, description="Correspondance des features")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Description de l'erreur")
    error_code: Optional[str] = Field(None, description="Code d'erreur spécifique")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de l'erreur")
    request_id: Optional[str] = Field(None, description="ID de la requête")


# Réponses pour l'interface web (simplifiées)
class WebPredictionResponse(BaseModel):
    """Réponse simplifiée pour l'interface web"""
    estimated_time_minutes: float = Field(..., description="Temps estimé en minutes")
    estimated_time_readable: str = Field(..., description="Temps lisible (ex: '25 min')")
    confidence: str = Field(..., description="Niveau de confiance (High/Medium/Low)")
    factors: Optional[Dict[str, str]] = Field(None, description="Facteurs influençant la prédiction")
    

class WebErrorResponse(BaseModel):
    """Réponse d'erreur pour l'interface web"""
    success: bool = Field(False, description="Succès de l'opération")
    message: str = Field(..., description="Message d'erreur utilisateur")
    technical_details: Optional[str] = Field(None, description="Détails techniques (mode debug)")
    suggestions: Optional[list] = Field(None, description="Suggestions pour corriger l'erreur")
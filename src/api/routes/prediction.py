
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
import logging

from ...utils.helpers import ResponseHelper
from ...services.prediction_service import PredictionService
from ..schemas.prediction import (
    DeliveryPredictionRequest,
    DeliveryPredictionResponse,
    RouteOptimizationRequest,
    RouteOptimizationResponse,
    DemandForecastRequest,
    DemandForecastResponse
)
from ..dependencies import get_prediction_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/delivery-time", response_model=DeliveryPredictionResponse)
async def predict_delivery_time(
    request: DeliveryPredictionRequest,
    prediction_service: PredictionService = Depends(get_prediction_service)
) -> DeliveryPredictionResponse:
    """Prédire le temps de livraison"""
    try:
        logger.info(f"Prédiction temps de livraison pour: {request.pickup_address} -> {request.delivery_address}")
        
        prediction = await prediction_service.predict_delivery_time(request)
        
        return DeliveryPredictionResponse(
            success=True,
            message="Prédiction réalisée avec succès",
            predicted_duration_minutes=prediction['duration_minutes'],
            estimated_arrival_time=prediction['estimated_arrival'],
            confidence_score=prediction['confidence'],
            factors=prediction['factors']
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction: {str(e)}"
        )

@router.post("/optimize-route", response_model=RouteOptimizationResponse)
async def optimize_route(
    request: RouteOptimizationRequest,
    prediction_service: PredictionService = Depends(get_prediction_service)
) -> RouteOptimizationResponse:
    """Optimiser un itinéraire de livraison"""
    try:
        logger.info(f"Optimisation de route pour {len(request.deliveries)} livraisons")
        
        optimization = await prediction_service.optimize_route(request)
        
        return RouteOptimizationResponse(
            success=True,
            message="Optimisation réalisée avec succès",
            optimized_route=optimization['route'],
            total_distance_km=optimization['total_distance'],
            estimated_total_time_minutes=optimization['total_time'],
            savings_vs_original=optimization['savings']
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'optimisation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'optimisation: {str(e)}"
        )

@router.post("/demand-forecast", response_model=DemandForecastResponse)
async def forecast_demand(
    request: DemandForecastRequest,
    prediction_service: PredictionService = Depends(get_prediction_service)
) -> DemandForecastResponse:
    """Prédire la demande de livraison"""
    try:
        logger.info(f"Prédiction de demande pour {request.zone} du {request.start_date} au {request.end_date}")
        
        forecast = await prediction_service.forecast_demand(request)
        
        return DemandForecastResponse(
            success=True,
            message="Prévision réalisée avec succès",
            zone=request.zone,
            forecasted_deliveries=forecast['forecasted_deliveries'],
            peak_hours=forecast['peak_hours'],
            confidence_interval=forecast['confidence_interval']
        )
    except Exception as e:
        logger.error(f"Erreur lors de la prévision: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prévision: {str(e)}"
        )
        
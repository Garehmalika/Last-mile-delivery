
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime


class PickupFeatures(BaseModel):
    accept_time: datetime = Field(..., description="Heure d'acceptation de la commande")
    time_window_start: datetime = Field(..., description="Début de la fenêtre de temps")
    time_window_end: datetime = Field(..., description="Fin de la fenêtre de temps")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    aoi_id: int = Field(..., description="ID de la zone d'intérêt")
    aoi_type: str = Field(..., description="Type de zone d'intérêt")
    pickup_time: datetime = Field(..., description="Heure de collecte")
    pickup_gps_time: datetime = Field(..., description="Heure GPS de collecte")
    pickup_gps_lng: float = Field(..., ge=-180, le=180, description="Longitude GPS de collecte")
    pickup_gps_lat: float = Field(..., ge=-90, le=90, description="Latitude GPS de collecte")
    accept_gps_time: datetime = Field(..., description="Heure GPS d'acceptation")
    accept_gps_lng: float = Field(..., ge=-180, le=180, description="Longitude GPS d'acceptation")
    accept_gps_lat: float = Field(..., ge=-90, le=90, description="Latitude GPS d'acceptation")
    ds: Optional[str] = Field(None, description="Date string optionnelle")
    waiting_time_minutes: float = Field(..., ge=0, description="Temps d'attente en minutes")
    city_encoded: int = Field(..., description="Code de la ville")
    
    @validator('time_window_end')
    def validate_time_window(cls, v, values):
        if 'time_window_start' in values and v <= values['time_window_start']:
            start_time = values['time_window_start']
            raise ValueError(
                f'time_window_end ({v}) doit être postérieur à time_window_start ({start_time}). '
                f'Différence actuelle: {(v - start_time).total_seconds()} secondes'
            )
        return v
   
    def to_model_input(self) -> Dict[str, Any]:
        """Convertit les features en format d'entrée pour le modèle"""
        return {
            'city_encoded': self.city_encoded,
            'lng': self.lng,
            'lat': self.lat,
            'aoi_id': self.aoi_id,
            'accept_time_seconds': self.accept_time.timestamp(),
            'time_window_start_seconds': self.time_window_start.timestamp(),
            'time_window_end_seconds': self.time_window_end.timestamp(),
            'pickup_time_seconds': self.pickup_time.timestamp(),
            'pickup_gps_time_seconds': self.pickup_gps_time.timestamp(),
            'pickup_gps_lng': self.pickup_gps_lng,
            'pickup_gps_lat': self.pickup_gps_lat,
            'accept_gps_time_seconds': self.accept_gps_time.timestamp(),
            'accept_gps_lng': self.accept_gps_lng,
            'accept_gps_lat': self.accept_gps_lat,
            'waiting_time_minutes': self.waiting_time_minutes
        }


class DeliveryFeatures(BaseModel):
    order_id: int = Field(..., description="ID de la commande")
    courier_id: int = Field(..., description="ID du coursier")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    aoi_id: int = Field(..., description="ID de la zone d'intérêt")
    accept_time_seconds: float = Field(..., description="Temps d'acceptation en secondes")
    accept_gps_time_seconds: float = Field(..., description="Temps GPS d'acceptation en secondes")
    accept_gps_lng: float = Field(..., ge=-180, le=180, description="Longitude GPS d'acceptation")
    accept_gps_lat: float = Field(..., ge=-90, le=90, description="Latitude GPS d'acceptation")
    delivery_time_seconds: float = Field(..., description="Temps de livraison en secondes")
    delivery_gps_time_seconds: float = Field(..., description="Temps GPS de livraison en secondes")
    delivery_gps_lng: float = Field(..., ge=-180, le=180, description="Longitude GPS de livraison")
    delivery_gps_lat: float = Field(..., ge=-90, le=90, description="Latitude GPS de livraison")
    delivery_time_minutes: float = Field(..., ge=0, description="Temps de livraison en minutes")
    accept_hour: int = Field(..., ge=0, le=23, description="Heure d'acceptation")
    accept_day: int = Field(..., ge=1, le=31, description="Jour d'acceptation")
    city_encoded: int = Field(..., description="Code de la ville")
    distance: float = Field(..., ge=0, description="Distance en km")
    day_of_week: int = Field(..., ge=0, le=6, description="Jour de la semaine")
    hour_of_day: int = Field(..., ge=0, le=23, description="Heure de la journée")
    task_duration_seconds: float = Field(..., ge=0, description="Durée de la tâche en secondes")
    log_task_duration: float = Field(..., description="Log de la durée de la tâche")
    delivery_hour: int = Field(..., ge=0, le=23, description="Heure de livraison")
    delivery_weekday: int = Field(..., ge=0, le=6, description="Jour de la semaine de livraison")
    task_duration_seconds_conv: float = Field(..., ge=0, description="Durée de la tâche convertie")

    def to_feature_array(self) -> list:
        """Convertit les features en array pour le modèle (sans order_id selon l'erreur)"""
        return [
            self.courier_id,
            self.lng,
            self.lat,
            self.aoi_id,
            self.accept_time_seconds,
            self.accept_gps_time_seconds,
            self.accept_gps_lng,
            self.accept_gps_lat,
            self.delivery_time_seconds,
            self.delivery_gps_time_seconds,
            self.delivery_gps_lng,
            self.delivery_gps_lat,
            self.delivery_time_minutes,
            self.accept_hour,
            self.accept_day,
            self.city_encoded,
            self.distance,
            self.day_of_week,
            self.hour_of_day,
            self.task_duration_seconds,
            self.log_task_duration,
            self.delivery_hour,
            self.delivery_weekday,
            self.task_duration_seconds_conv
        ]


# Schémas simplifiés pour l'interface web
class SimplePickupRequest(BaseModel):
    """Version simplifiée pour l'interface web"""
    pickup_address: str = Field(..., description="Adresse de collecte")
    delivery_address: str = Field(..., description="Adresse de livraison")
    scheduled_time: datetime = Field(..., description="Heure prévue")
    city: str = Field(..., description="Ville")
    
    
class SimpleDeliveryRequest(BaseModel):
    """Version simplifiée pour l'interface web"""
    order_id: int = Field(..., description="Numéro de commande")
    pickup_address: str = Field(..., description="Adresse de collecte")
    delivery_address: str = Field(..., description="Adresse de livraison")
    courier_name: str = Field(..., description="Nom du coursier")
    city: str = Field(..., description="Ville")
    distance_km: float = Field(..., ge=0, description="Distance estimée en km")

# src/utils/validators.py
from typing import Optional, Tuple, List, Dict, Any
import re
from datetime import datetime, timedelta
from pydantic import BaseModel, validator

class LocationValidator:
    """Validateur pour les coordonnées géographiques"""
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """Valide les coordonnées GPS"""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """Valide le format d'une adresse"""
        return len(address.strip()) >= 10

class DeliveryValidator:
    """Validateur pour les données de livraison"""
    
    @staticmethod
    def validate_delivery_time(delivery_time: str) -> bool:
        """Valide le format du temps de livraison"""
        try:
            datetime.fromisoformat(delivery_time.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_weight(weight: float) -> bool:
        """Valide le poids du colis (en kg)"""
        return 0 < weight <= 50  # Max 50kg
    
    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Valide le niveau de priorité"""
        return priority.upper() in ['LOW', 'MEDIUM', 'HIGH', 'URGENT']

class DataValidator:
    """Validateur général pour les données"""
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valide un numéro de téléphone"""
        pattern = r'^[\+]?[1-9][\d]{0,15}$'
        return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valide une adresse email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

# ============================================================================

# src/utils/helpers.py
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json

class DateTimeHelper:
    """Utilitaires pour les dates et heures"""
    
    @staticmethod
    def now() -> datetime:
        """Retourne l'heure actuelle"""
        return datetime.utcnow()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Formate une datetime en string"""
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(dt_str: str) -> datetime:
        """Parse une string en datetime"""
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """Ajoute des heures à une datetime"""
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def business_hours_only(dt: datetime) -> datetime:
        """Ajuste une datetime pour être dans les heures ouvrables"""
        # Si weekend, passer au lundi
        if dt.weekday() >= 5:  # Samedi = 5, Dimanche = 6
            days_until_monday = 7 - dt.weekday()
            dt = dt + timedelta(days=days_until_monday)
        
        # Si avant 8h, mettre à 8h
        if dt.hour < 8:
            dt = dt.replace(hour=8, minute=0, second=0, microsecond=0)
        # Si après 18h, passer au jour suivant à 8h
        elif dt.hour >= 18:
            dt = dt + timedelta(days=1)
            dt = dt.replace(hour=8, minute=0, second=0, microsecond=0)
        
        return dt

class SecurityHelper:
    """Utilitaires de sécurité"""
    
    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """Génère une clé API sécurisée"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash un mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Vérifie un mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed

class DataHelper:
    """Utilitaires pour les données"""
    
    @staticmethod
    def safe_dict_get(data: Dict, key: str, default: Any = None) -> Any:
        """Récupère une valeur de dictionnaire de manière sécurisée"""
        return data.get(key, default) if isinstance(data, dict) else default
    
    @staticmethod
    def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Aplatit un dictionnaire imbriqué"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataHelper.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2) -> float:
        """Calcule la distance entre deux points GPS (en km)"""
        from math import radians, cos, sin, asin, sqrt
        
        # Convertir en radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Formule haversine
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Rayon de la Terre en km
        
        return c * r
    
    @staticmethod
    def chunk_list(lst: List, chunk_size: int) -> List[List]:
        """Divise une liste en chunks"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

class ResponseHelper:
    """Utilitaires pour les réponses API"""
    
    @staticmethod
    def success_response(data: Any = None, message: str = "Success") -> Dict:
        """Génère une réponse de succès standardisée"""
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": DateTimeHelper.now().isoformat()
        }
    
    @staticmethod
    def error_response(message: str, error_code: str = None, details: Any = None) -> Dict:
        """Génère une réponse d'erreur standardisée"""
        return {
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": details,
            "timestamp": DateTimeHelper.now().isoformat()
        }
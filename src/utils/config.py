# src/utils/config.py
import os

from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Charger les variables d'environnement
load_dotenv()

@dataclass
class Config:
    """Configuration de l'application"""
    # Chemins des modèles
    PICKUP_MODEL_PATH: str = "models/lasso_model_pickup.pkl"
    DELIVERY_MODEL_PATH: str = "models/lasso_model.pkl"
    DATA_DIR: str = "data"
    LOGS_DIR: str = "monitoring/logs"
    
    # Configuration API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 1
    
    # Configuration base de données (si nécessaire)
    DATABASE_URL: str = ""
    
    # Configuration logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuration cache
    CACHE_TTL: int = 3600  # 1 heure
    
    # Configuration sécurité
    API_KEY: str = ""
    
    def __post_init__(self):
        """Charge la configuration depuis les variables d'environnement"""
        self.PICKUP_MODEL_PATH = os.getenv("PICKUP_MODEL_PATH", self.PICKUP_MODEL_PATH)
        self.DELIVERY_MODEL_PATH = os.getenv("DELIVERY_MODEL_PATH", self.DELIVERY_MODEL_PATH)
        self.DATA_DIR = os.getenv("DATA_DIR", self.DATA_DIR)
        self.LOGS_DIR = os.getenv("LOGS_DIR", self.LOGS_DIR)
        
        self.API_HOST = os.getenv("API_HOST", self.API_HOST)
        self.API_PORT = int(os.getenv("API_PORT", str(self.API_PORT)))
        self.API_WORKERS = int(os.getenv("API_WORKERS", str(self.API_WORKERS)))
        
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", self.LOG_LEVEL)
        
        self.CACHE_TTL = int(os.getenv("CACHE_TTL", str(self.CACHE_TTL)))
        
        self.API_KEY = os.getenv("API_KEY", self.API_KEY)


# Instance globale de configuration
_config = None

def get_settings() -> Config:
    """Retourne l'instance de configuration (singleton)"""
    global _config
    if _config is None:
        _config = Config()
    return _config

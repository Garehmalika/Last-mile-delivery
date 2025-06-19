from fastapi import APIRouter, Depends
from typing import Dict
import psutil
import time
from datetime import datetime

from ...utils.helpers import ResponseHelper
from ...utils.config import config

router = APIRouter()

@router.get("/")
async def health_check() -> Dict:
    """Vérification de santé basique"""
    return ResponseHelper.success_response(
        data={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": config.app_version
        },
        message="Service is healthy"
    )

@router.get("/detailed")
async def detailed_health_check() -> Dict:
    """Vérification de santé détaillée"""
    try:
        # Métriques système
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Vérification de la base de données (à implémenter)
        database_status = "connected"  # Placeholder
        
        # Vérification des services externes
        external_services = {
            "google_maps": "available" if config.google_maps_api_key else "not_configured",
            "weather_api": "available" if config.weather_api_key else "not_configured"
        }
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": config.app_version,
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "disk_percent": (disk.used / disk.total) * 100,
                "disk_free": disk.free
            },
            "services": {
                "database": database_status,
                "external_apis": external_services
            }
        }
        
        return ResponseHelper.success_response(
            data=health_data,
            message="Detailed health check completed"
        )
        
    except Exception as e:
        return ResponseHelper.error_response(
            message="Health check failed",
            error_code="HEALTH_CHECK_ERROR",
            details=str(e)
        )

@router.get("/ready")
async def readiness_check() -> Dict:
    """Vérification de préparation (K8s readiness probe)"""
    # Vérifier que tous les services critiques sont prêts
    checks = {
        "database": True,  # À implémenter
        "models_loaded": True,  # À implémenter
        "external_apis": bool(config.google_maps_api_key)
    }
    
    is_ready = all(checks.values())
    
    return ResponseHelper.success_response(
        data={
            "ready": is_ready,
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        },
        message="Ready" if is_ready else "Not ready"
    )

@router.get("/live")
async def liveness_check() -> Dict:
    """Vérification de vivacité (K8s liveness probe)"""
    return ResponseHelper.success_response(
        data={
            "alive": True,
            "timestamp": datetime.utcnow().isoformat()
        },
        message="Service is alive"
    )
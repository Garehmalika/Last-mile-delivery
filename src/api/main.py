from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
from .routes import prediction, health, monitoring
from .middleware.cors import setup_cors
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('templates/dashboard.html')

@main_bp.route('/prediction', methods=['POST'])
def predict():
    # Logique de prédiction
    pass
# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Last Mile Delivery ETA Prediction API",
    description="API pour prédire l'ETA des livraisons de dernière minute",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
setup_cors(app)

# Inclusion des routes
app.include_router(prediction.router, prefix="/predict", tags=["predictions"])
app.include_router(health.router, tags=["health"])
app.include_router(monitoring.router, prefix="/debug", tags=["monitoring"])

@app.get("/")
def root():
    """Route racine de l'API"""
    return {
        "message": "API Last Mile Delivery ETA Prediction opérationnelle",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Gestionnaire d'erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Gestionnaire personnalisé pour les erreurs de validation"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Erreur de validation des données d'entrée",
            "tips": {
                "time_window": "Assurez-vous que time_window_end > time_window_start",
                "coordinates": "Latitude doit être entre -90 et 90, Longitude entre -180 et 180",
                "datetime_format": "Format attendu: 'YYYY-MM-DDTHH:MM:SS' (ISO 8601)"
            }
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": [{
                "type": "value_error",
                "loc": ["body"],
                "msg": str(exc),
                "input": None
            }]
        }
    )
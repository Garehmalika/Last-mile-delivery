import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

from .prediction_service import model_manager  # Importer le model_manager existant

logger = logging.getLogger(__name__)

# Liste des features attendues par le modèle de livraison, copiée de prediction_service.py
DELIVERY_FEATURE_NAMES = [
    'courier_id', 'lng', 'lat', 'aoi_id',
    'accept_time_seconds', 'accept_gps_time_seconds', 'accept_gps_lng', 'accept_gps_lat',
    'delivery_time_seconds', 'delivery_gps_time_seconds', 'delivery_gps_lng', 'delivery_gps_lat',
    'delivery_time_minutes', 'accept_hour', 'accept_day', 'city_encoded', 'distance',
    'day_of_week', 'hour_of_day', 'task_duration_seconds', 'log_task_duration',
    'delivery_hour', 'delivery_weekday', 'task_duration_seconds_conv'
]

def geocode_address(address: str):
    """
    Fonction de simulation pour convertir une adresse en coordonnées (lat, lng)
    et en distance approximative.
    Dans une vraie application, on utiliserait une API comme Google Maps.
    """
    # Simulation basée sur le nom de l'adresse pour la démo
    if "Shanghai" in address.lower():
        return 48.8566, 2.3522
    elif "Hangzhou" in address.lower():
        return 45.7640, 4.8357
    elif "Jilin" in address.lower():
        return 43.2965, 5.3698
    elif "Chongqing" in address.lower():
        return 30.5728, 114.2794
    elif "Yantai" in address.lower():
        return 39.9087, 116.3975
    else:
        # Valeurs par défaut
        return 48.86, 2.36 + np.random.rand() * 0.1 # Autour de Paris

def calculate_distance(pickup_coords, delivery_coords):
    """
    Calcule une distance euclidienne approximative.
    Ne remplace pas un vrai calcul de distance routière.
    """
    return np.sqrt((pickup_coords[0] - delivery_coords[0])**2 + (pickup_coords[1] - delivery_coords[1])**2) * 100


def predict_delivery_time_simplified(form_data: dict):
    """
    Prépare les données à partir du formulaire web et prédit le temps de livraison.
    """
    if not model_manager.is_delivery_available():
        raise RuntimeError("Le modèle de prédiction de livraison n'est pas chargé.")

    # --- 1. Préparation des features à partir des données du formulaire ---

    now = datetime.now()
    pickup_lat, pickup_lng = geocode_address(form_data['pickup_address'])
    delivery_lat, delivery_lng = geocode_address(form_data['delivery_address'])
    
    distance = calculate_distance((pickup_lat, pickup_lng), (delivery_lat, delivery_lng))

    # --- 2. Création de features simulées pour correspondre au modèle ---
    
    # Créer un dictionnaire avec des valeurs par défaut pour toutes les features
    feature_dict = {feature: 0.0 for feature in DELIVERY_FEATURE_NAMES}
    
    # Remplacer avec les valeurs que nous pouvons calculer ou simuler
    feature_dict.update({
        'distance': distance,
        'lat': delivery_lat,
        'lng': delivery_lng,
        'delivery_gps_lat': delivery_lat,
        'delivery_gps_lng': delivery_lng,
        'accept_gps_lat': pickup_lat,
        'accept_gps_lng': pickup_lng,
        'delivery_time_minutes': 30,  # Valeur de base qui pourrait être ajustée
        'hour_of_day': now.hour,
        'day_of_week': now.weekday(),
        'delivery_hour': now.hour,
        'delivery_weekday': now.weekday(),
        'accept_hour': now.hour,
        'accept_day': now.day,
        'courier_id': 100,  # Simulé
        'aoi_id': 1, # Simulé
        'city_encoded': 1 if "paris" in form_data['delivery_address'].lower() else 2, # Simulé
        
        # Simulation des timestamps en secondes
        'accept_time_seconds': (now - datetime(1970, 1, 1)).total_seconds(),
        'delivery_time_seconds': (now - datetime(1970, 1, 1)).total_seconds() + 1800, # +30 mins
    })

    # --- 3. Création du DataFrame pour le modèle ---
    
    # Créer le DataFrame avec les colonnes dans le bon ordre
    input_df = pd.DataFrame([feature_dict], columns=DELIVERY_FEATURE_NAMES)
    
    # S'assurer que les colonnes correspondent exactement à celles du modèle
    if hasattr(model_manager.model_delivery, 'feature_names_in_'):
        model_features = list(model_manager.model_delivery.feature_names_in_)
        input_df = input_df.reindex(columns=model_features, fill_value=0)
    else:
        # Si le modèle n'a pas cette information, on utilise notre liste
        input_df = input_df[DELIVERY_FEATURE_NAMES]

    # --- 4. Prédiction ---
    
    try:
        prediction_array = model_manager.model_delivery.predict(input_df)
        predicted_time_minutes = float(prediction_array[0])

        # Ajouter des ajustements basés sur le formulaire pour rendre la démo plus crédible
        if form_data['traffic_level'] == 'high':
            predicted_time_minutes += 10
        if form_data['weather_condition'] == 'rainy':
            predicted_time_minutes += 5
        if form_data['package_type'] == 'urgent':
            predicted_time_minutes = max(10, predicted_time_minutes - 10)
            
        return {
            'estimated_time': abs(predicted_time_minutes), # S'assurer que le temps est positif
            'confidence': 0.85, # Score de confiance fixe pour la démo
            'route_distance': distance,
            'factors': {
                 'traffic_impact': '+10 min' if form_data['traffic_level'] == 'high' else '0 min',
                 'weather_impact': '+5 min' if form_data['weather_condition'] == 'rainy' else '0 min',
                 'package_impact': '-10 min' if form_data['package_type'] == 'urgent' else '0 min'
            }
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction simplifiée: {e}")
        raise 

def predict_pickup_time_simplified(form_data: dict):
    """
    Traduit les données du formulaire pour le modèle pickup
    puis renvoie la prédiction en minutes.
    """
    if not model_manager.is_pickup_available():
        raise RuntimeError("Modèle pickup non chargé")

    now = datetime.now()
    # On peut ré-utiliser le geocode + distance si nécessaire
    pickup_lat, pickup_lng = geocode_address(form_data['pickup_address'])

    # ---------------------------
    # 1. Préparer les features attendues par model_pickup
    # ---------------------------
    input_data = {
        "accept_time": now,
        "time_window_start": now,
        "time_window_end": now + timedelta(minutes=30),
        "lng": pickup_lng,
        "lat": pickup_lat,
        "aoi_id": 1,
        "aoi_type": "pickup",
        "pickup_time": now,
        "pickup_gps_time": now,
        "pickup_gps_lng": pickup_lng,
        "pickup_gps_lat": pickup_lat,
        "accept_gps_time": now,
        "accept_gps_lng": pickup_lng,
        "accept_gps_lat": pickup_lat,
        "waiting_time_minutes": 0,
        "city_encoded": 1,
    }

    # 2. Pydantic : construire l'objet `PickupFeatures`
    from src.api.schemas.prediction import PickupFeatures
    features = PickupFeatures(**input_data)

    # 3. Appeler le modèle
    result = model_manager.predict_pickup(features)
    return {
        "estimated_time": result["prediction"],
        "confidence": result["confidence_score"],
        "factors": {},       # à compléter si besoin
    }
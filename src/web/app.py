from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import os
import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
from src.services.simplified_prediction_service import predict_delivery_time_simplified
from src.services.simplified_prediction_service import predict_pickup_time_simplified
from flask import Flask, render_template, request, jsonify
from src.web.routes.main import main_bp
from src.web.routes.dashboard import dashboard_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


app.register_blueprint(main_bp)
app.register_blueprint(dashboard_bp)


# Configuration API
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')

# Formulaire de prédiction de livraison
class DeliveryPredictionForm(FlaskForm):
    pickup_address = StringField('Adresse de collecte', validators=[DataRequired()])
    delivery_address = StringField('Adresse de livraison', validators=[DataRequired()])
    package_weight = FloatField('Poids du colis (kg)', validators=[DataRequired(), NumberRange(min=0.1, max=50)])
    package_type = SelectField('Type de colis', 
                              choices=[('standard', 'Standard'), ('fragile', 'Fragile'), ('urgent', 'Urgent')],
                              validators=[DataRequired()])
    weather_condition = SelectField('Conditions météo',
                                   choices=[('sunny', 'Ensoleillé'), ('rainy', 'Pluvieux'), ('cloudy', 'Nuageux')],
                                   validators=[DataRequired()])
    traffic_level = SelectField('Niveau de trafic',
                               choices=[('low', 'Faible'), ('medium', 'Moyen'), ('high', 'Élevé')],
                               validators=[DataRequired()])
    prediction_type = SelectField('Type de prédiction',
                                 choices=[('delivery', 'Delivery Time'), ('pickup', 'Pickup Time')],
                                 validators=[DataRequired()])
    submit = SubmitField('Prédire')

# Formulaire d'optimisation de route
class RouteOptimizationForm(FlaskForm):
    start_location = StringField('Point de départ', validators=[DataRequired()])
    destinations = StringField('Destinations (séparées par des virgules)', validators=[DataRequired()])
    vehicle_type = SelectField('Type de véhicule',
                              choices=[('bike', 'Vélo'), ('scooter', 'Scooter'), ('van', 'Camionnette')],
                              validators=[DataRequired()])
    max_capacity = FloatField('Capacité maximale (kg)', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField('Optimiser la route')

@app.route('/')
def index():
    """Page d'accueil avec statistiques générales"""
    # Données simulées pour la démo
    stats = {
        'total_deliveries': 1247,
        'avg_delivery_time': 28.5,
        'success_rate': 97.8,
        'active_drivers': 23
    }
    return render_template('index.html', stats=stats)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    """Page de prédiction de temps de livraison"""
    form = DeliveryPredictionForm()
    prediction_result = None
    
    if form.validate_on_submit():
        # Données à envoyer à l'API
        data = {
            'pickup_address': form.pickup_address.data,
            'delivery_address': form.delivery_address.data,
            'package_weight': form.package_weight.data,
            'package_type': form.package_type.data,
            'weather_condition': form.weather_condition.data,
            'traffic_level': form.traffic_level.data,
            'prediction_type': form.prediction_type.data
        }
        
        try:
            # Appel au service de prédiction approprié
            if form.prediction_type.data == 'pickup':
                prediction_result = predict_pickup_time_simplified(data)
            else:
                prediction_result = predict_delivery_time_simplified(data)
            
        except Exception as e:
            flash(f'Erreur lors de la prédiction: {str(e)}', 'error')
    
    return render_template('prediction.html', form=form, result=prediction_result)

@app.route('/route-optimization', methods=['GET', 'POST'])
def route_optimization():
    """Page d'optimisation de route"""
    form = RouteOptimizationForm()
    optimization_result = None
    
    if form.validate_on_submit():
        destinations = [dest.strip() for dest in form.destinations.data.split(',')]
        
        data = {
            'start_location': form.start_location.data,
            'destinations': destinations,
            'vehicle_type': form.vehicle_type.data,
            'max_capacity': form.max_capacity.data
        }
        
        try:
            # Simulation de réponse pour la démo
            import random
            optimization_result = {
                'optimized_route': [form.start_location.data] + random.sample(destinations, len(destinations)),
                'total_distance': round(random.uniform(15, 50), 1),
                'estimated_time': random.randint(45, 180),
                'fuel_cost': round(random.uniform(12, 35), 2),
                'savings': {
                    'distance_saved': round(random.uniform(2, 8), 1),
                    'time_saved': random.randint(10, 30),
                    'cost_saved': round(random.uniform(3, 12), 2)
                }
            }
            
        except Exception as e:
            flash(f'Erreur lors de l\'optimisation: {str(e)}', 'error')
    
    return render_template('route_optimization.html', form=form, result=optimization_result)

@app.route('/api/health')
def health_check():
    """Endpoint de santé pour l'application web"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/stats')
def get_stats():
    """API pour récupérer les statistiques en temps réel"""
    import random
    stats = {
        'deliveries_today': random.randint(70, 90),
        'avg_delivery_time': round(random.uniform(20, 35), 1),
        'success_rate': round(random.uniform(95, 99), 1),
        'active_drivers': random.randint(15, 25)
    }
    return jsonify(stats)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='127.0.0.1', port=port, debug=debug)
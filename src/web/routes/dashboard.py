from flask import Blueprint, render_template, jsonify
from datetime import datetime
import random

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Dashboard avec métriques et graphiques"""
    # Données simulées pour les graphiques
    
    # Graphique des livraisons par heure
    hours = list(range(24))
    deliveries_by_hour = [max(0, 20 + 15 * __import__('math').sin(h/24 * 2 * 3.14159) + __import__('random').randint(-5, 5)) for h in hours]
    
    deliveries_chart = {
        'data': [{
            'x': hours,
            'y': deliveries_by_hour,
            'type': 'bar',
            'name': 'Livraisons',
            'marker': {'color': '#3498db'}
        }],
        'layout': {
            'title': 'Livraisons par heure',
            'xaxis': {'title': 'Heure'},
            'yaxis': {'title': 'Nombre de livraisons'}
        }
    }
    
    # Graphique de performance des chauffeurs
    drivers = ['Driver A', 'Driver B', 'Driver C', 'Driver D', 'Driver E']
    performance = [95, 87, 92, 88, 94]
    
    performance_chart = {
        'data': [{
            'x': drivers,
            'y': performance,
            'type': 'bar',
            'name': 'Performance',
            'marker': {'color': '#2ecc71'}
        }],
        'layout': {
            'title': 'Performance des chauffeurs (%)',
            'xaxis': {'title': 'Chauffeurs'},
            'yaxis': {'title': 'Taux de réussite (%)'}
        }
    }
    
    # Graphique temporel des livraisons
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    daily_deliveries = [__import__('random').randint(40, 80) for _ in dates]
    
    timeline_chart = {
        'data': [{
            'x': dates,
            'y': daily_deliveries,
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Livraisons quotidiennes',
            'line': {'color': '#e74c3c'}
        }],
        'layout': {
            'title': 'Évolution des livraisons (30 derniers jours)',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Nombre de livraisons'}
        }
    }
    
    # Métriques KPI
    kpis = {
        'total_deliveries_today': 87,
        'avg_delivery_time_today': 26.3,
        'success_rate_today': 98.9,
        'active_drivers_now': 18,
        'pending_deliveries': 23,
        'completed_deliveries': 64
    }
    
    return render_template('dashboard.html', 
                          deliveries_chart=json.dumps(deliveries_chart),
                          performance_chart=json.dumps(performance_chart),
                          timeline_chart=json.dumps(timeline_chart),
                          kpis=kpis)

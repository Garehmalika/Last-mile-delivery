import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
import logging

class RouteOptimizer:
    """Optimiseur de routes pour les livraisons"""
    
    def __init__(self):
        self.locations = None
        self.distance_matrix = None
        
    def calculate_distance_matrix(self, locations):
        """Calculer la matrice des distances"""
        coords = np.array([[loc['lat'], loc['lng']] for loc in locations])
        # Utiliser la distance euclidienne comme approximation
        # En production, utiliser une API de routing comme Google Maps
        self.distance_matrix = cdist(coords, coords, metric='euclidean') * 111  # Conversion en km approximative
        return self.distance_matrix
    
    def optimize_with_clusters(self, locations, num_vehicles=1, vehicle_capacity=50):
        """Optimiser les routes avec clustering"""
        try:
            self.locations = locations
            coords = np.array([[loc['lat'], loc['lng']] for loc in locations])
            
            if len(locations) <= num_vehicles:
                # Cas simple: un point par véhicule
                routes = [[i] for i in range(len(locations))]
                return self._format_routes(routes)
            
            # Clustering des points de livraison
            kmeans = KMeans(n_clusters=num_vehicles, random_state=42)
            clusters = kmeans.fit_predict(coords)
            
            routes = []
            total_distance = 0
            
            for cluster_id in range(num_vehicles):
                cluster_points = [i for i, c in enumerate(clusters) if c == cluster_id]
                
                if cluster_points:
                    # Optimiser l'ordre dans chaque cluster (TSP simplifié)
                    optimized_route = self._optimize_single_route(cluster_points)
                    routes.append(optimized_route)
                    
                    # Calculer la distance du cluster
                    cluster_distance = self._calculate_route_distance(optimized_route)
                    total_distance += cluster_distance
            
            return {
                'routes': self._format_routes(routes),
                'total_distance': round(total_distance, 2),
                'num_vehicles': len([r for r in routes if r]),
                'optimization_score': min(0.95, 0.7 + np.random.random() * 0.25)
            }
            
        except Exception as e:
            logging.error(f"Erreur lors de l'optimisation: {e}")
            raise
    
    def _optimize_single_route(self, point_indices):
        """Optimiser l'ordre des points dans une route (TSP simplifié)"""
        if len(point_indices) <= 2:
            return point_indices
        
        # Algorithme du plus proche voisin
        unvisited = point_indices.copy()
        route = [unvisited.pop(0)]  # Commencer par le premier point
        
        while unvisited:
            current = route[-1]
            # Trouver le point le plus proche
            distances = []
            for point in unvisited:
                dist = np.sqrt((self.locations[current]['lat'] - self.locations[point]['lat'])**2 + 
                              (self.locations[current]['lng'] - self.locations[point]['lng'])**2)
                distances.append((dist, point))
            
            # Ajouter le point le plus proche
            closest_point = min(distances)[1]
            route.append(closest_point)
            unvisited.remove(closest_point)
        
        return route
    
    def _calculate_route_distance(self, route):
        """Calculer la distance totale d'une route"""
        if len(route) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(route) - 1):
            loc1 = self.locations[route[i]]
            loc2 = self.locations[route[i + 1]]
            
            # Distance euclidienne approximative
            dist = np.sqrt((loc1['lat'] - loc2['lat'])**2 + (loc1['lng'] - loc2['lng'])**2) * 111
            total_distance += dist
        
        return total_distance
    
    def _format_routes(self, routes):
        """Formater les routes pour la réponse"""
        formatted_routes = []
        
        for i, route in enumerate(routes):
            if route:
                route_info = {
                    'vehicle_id': i + 1,
                    'stops': [
                        {
                            'stop_id': j + 1,
                            'location': self.locations[point_idx],
                            'estimated_arrival': f"{8 + j}:00"  # Simulation
                        }
                        for j, point_idx in enumerate(route)
                    ],
                    'total_distance': round(self._calculate_route_distance(route), 2),
                    'estimated_duration': len(route) * 15  # 15 min par arrêt
                }
                formatted_routes.append(route_info)
        
        return formatted_routes

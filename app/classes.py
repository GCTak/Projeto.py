import math

class Neighborhood:
    def __init__(self, name, latitude, longitude, city=None):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("O nome do bairro deve ser uma string não vazia.")
        self.name = name
        
        if not (-90 <= latitude <= 90):
            raise ValueError("A latitude deve estar entre -90 e 90 graus.")
        self.latitude = latitude
        
        if not (-180 <= longitude <= 180):
            raise ValueError("A longitude deve estar entre -180 e 180 graus.")
        self.longitude = longitude

        if city:
            if not isinstance(city, str) or len(city.strip()) == 0:
                raise ValueError("O nome da cidade deve ser uma string não vazia.")
            self.city = city

    def __str__(self):
        if hasattr(self, 'city'):
            return f"Nome: {self.name} - Latitude: {self.latitude} - Longitude: {self.longitude} - Cidade: {self.city}"
        else:
            return f"Nome: {self.name} - Latitude: {self.latitude} - Longitude: {self.longitude}"

    def __repr__(self):
        if hasattr(self, 'city'):
            return f"{self.name} - {self.latitude} - {self.longitude} - {self.city}"
        return f"{self.name} - {self.latitude} - {self.longitude}"
    

    def distance_to(self, other):
        """
        Calcula a distância entre dois bairros usando a fórmula de Haversine.
        Retorna a distância em quilômetros.
        """
        # Raio da Terra em quilômetros
        R = 6371.0

        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.latitude)
        lon2 = math.radians(other.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

class Node:
    def __init__(self, neighborhood):
        self.neighborhood = neighborhood
        self.adjacent_nodes = []

    def add_edge(self, node):
        """
        Adiciona uma aresta para um nó adjacente.
        """
        self.adjacent_nodes.append(node)

    def __str__(self):
        return f"Node: {self.neighborhood}"

    def __repr__(self):
        return f"Node: {self.neighborhood}"

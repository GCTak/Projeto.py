import math
import heapq

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
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("O nome do bairro deve ser uma string não vazia.")
        self.name = name

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
        self.adjacent_nodes = {}
    @property
    def name(self):
        return self.neighborhood.name
    
    def add_edge(self, node, weight=1):
        """
        Adiciona uma aresta para um nó adjacente com um peso específico.
        """
        self.adjacent_nodes[node] = weight

    def remove_edge(self, node):
        """
        Remove uma aresta para um nó adjacente.
        """
        if node in self.adjacent_nodes:
            del self.adjacent_nodes[node]

    def __str__(self):
        if self.adjacent_nodes:
            return f"Node: {self.neighborhood} - Adjacentes: {[neighbor.neighborhood.name for neighbor in self.adjacent_nodes]}"
        else:
            return f"Node: {self.neighborhood}"

    def __repr__(self):
        if self.adjacent_nodes:
            return f"{self.neighborhood} - {[neighbor.neighborhood.name for neighbor in self.adjacent_nodes]}"
        else:
            return f"Node: {self.neighborhood}"

class Graph:
    def __init__(self):
        self.nodes = []
    
    def add_node(self, node):
        """
        Adiciona um nó ao grafo.
        """
        self.nodes.append(node)

    def remove_node(self, node):
        """
        Remove um nó do grafo.
        """
        self.nodes.remove(node)
        for n in self.nodes:
            n.remove_edge(node)

    def add_edge(self, node_a, node_b, weight=1):
        """
        Adiciona uma aresta entre dois nós com um peso específico.
        """
        node_a.add_edge(node_b, weight)
        node_b.add_edge(node_a, weight)

    def remove_edge(self, node_a, node_b):
        """
        Remove uma aresta entre dois nós.
        """
        node_a.remove_edge(node_b)
        node_b.remove_edge(node_a)

    def get_node(self, name):
        """
        Retorna um nó específico do grafo.
        """
        for node in self.nodes:
            if node.neighborhood.name == name:
                return node
        return None

    def set_weight(self, node_a, node_b, weight):
        """
        Define o peso de uma aresta entre dois nós.
        """
        if node_b in node_a.adjacent_nodes:
            node_a.adjacent_nodes[node_b] = weight
        if node_a in node_b.adjacent_nodes:
            node_b.adjacent_nodes[node_a] = weight
    
    def print_weights(self):
        for node in self.nodes:
            print(f"Node: {node.neighborhood.name}")
            for neighbor, weight in node.adjacent_nodes.items():
                print(f"Vizinho: {neighbor.neighborhood.name} - Peso: {weight}")

    def print_weight(self, node_a, node_b):
        if node_b in node_a.adjacent_nodes:
            print(f"Peso da aresta entre {node_a.neighborhood.name} e {node_b.neighborhood.name}: {node_a.adjacent_nodes[node_b]}")
        else:
            print(f"Não há uma aresta entre {node_a.neighborhood.name} e {node_b.neighborhood.name}.")

    def adjacent_matrix(self):
            """
            Retorna a matriz de adjacência do grafo junto com os nomes dos nós.
            """
            matrix = []
            node_names = [node.neighborhood.name for node in self.nodes]
            for node in self.nodes:

                row = []
                for neighbor in self.nodes:
                    if neighbor in node.adjacent_nodes:
                        row.append(1)
                    else:
                        row.append(0)
                matrix.append(row)
            return node_names, matrix
    

    def set_cost_automaticaly(self, cost_for_km_of_the_segment):
        for node in self.nodes:
            for neighbor in node.adjacent_nodes:
                distance = node.neighborhood.distance_to(neighbor.neighborhood)
                cost = distance * cost_for_km_of_the_segment
                self.set_weight(node, neighbor, cost)
        print("Custo calculado automaticamente para todas as arestas do grafo.")

    def __str__(self):
        return f"Nodes: {[node.neighborhood.name for node in self.nodes]}"

    def __repr__(self):
        return f"{[node.neighborhood.name for node in self.nodes]}"
    
    def get_adjacent_nodes(self, node):
        """
        Retorna todos os nós adjacentes a um nó específico.
        """
        return node.adjacent_nodes

    def get_edge_weight(self, node_a, node_b):
        """
        Retorna o peso da aresta entre dois nós específicos.
        """
        for edge in node_a.adjacent_nodes:
            if edge.neighborhood == node_b:
                return edge.weight
        return None

    def edge_exists(self, node_a, node_b):
        """
        Verifica se uma aresta existe entre dois nós específicos.
        """
        return any(edge.neighborhood == node_b for edge in node_a.adjacent_nodes)


class Segment:
    def __init__(self, segment_a, segment_b, cost_per_km=1):
        #Segmento A se refere ao bairro de origem
        self.segment_a = segment_a
        self.segment_b = segment_b
        self.cost_per_km = cost_per_km

        distance = segment_a.distance_to(segment_b)
        self.weight = distance * cost_per_km

    def set_cost(self, cost_per_km):
        self.cost_per_km = cost_per_km
        distance = self.segment_a.distance_to(self.segment_b)
        self.weight = distance * cost_per_km

    def get_cost(self):
        return self.cost_per_km
    
    def get_weight(self):
        return self.weight
    
    def get_segment_a(self):
        return self.segment_a
    
    def get_segment_b(self):
        return self.segment_b
    
    def set_segment_a(self, segment_a):
        self.segment_a = segment_a
        distance = segment_a.distance_to(self.segment_b)
        self.weight = distance * self.cost_per_km

    def set_segment_b(self, segment_b):
        self.segment_b = segment_b
        distance = self.segment_a.distance_to(segment_b)
        self.weight = distance * self.cost_per_km
    
    def __str__(self):
        return "Segmento de rede entre {} e {} com custo de R${:.2f}, sendo R${:.2F}/km de custo.".format(self.segment_a, self.segment_b, self.weight, self.cost_per_km)

    def __repr__(self):
        return f"{self.segment_a} - {self.segment_b} - {self.cost_per_km}"
    
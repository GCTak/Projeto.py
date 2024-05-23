#encoding: utf-8
import os
import networkx as nx
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point
from classes import Neighborhood, Node, Graph, Segment
import json
import heapq
import numpy as np

INVALID_OPTION = "Opção inválida"

def load_neighborhoods():
    try:
        # check if the file exists
        if os.path.exists('neighborhoods.json'):
            with open('neighborhoods.json', 'r') as file:
                neighborhoods_data = json.load(file)
                neighborhoods = []
                # the data is organized as Name, Coordinates (lat,lon), City
                for neighborhood in neighborhoods_data:
                    name = neighborhood["Name"]
                    coordinates = neighborhood["Coordinates"]
                    lat, long = coordinates.split(',')
                    city = neighborhood.get("City")  # Use get to safely access the key

                    neighborhood_obj = Neighborhood(name, float(lat), float(long), city)
                    neighborhoods.append(neighborhood_obj)
                    
            return neighborhoods
    except Exception as e:
        print(e)
        return False

def load_segments(neighborhoods):
    try:
        if os.path.exists('network_segments.json'):
            with open('network_segments.json', 'r') as file:
                segments_data = json.load(file)
                segments = []
                for segment in segments_data:
                    segment_a_name = segment["from"]
                    segment_b_name = segment["to"]
                    cost_per_km = segment["cost_per_km"]

                    # Encontre os objetos de bairro correspondentes
                    segment_a = next((n for n in neighborhoods if n.name == segment_a_name), None)
                    segment_b = next((n for n in neighborhoods if n.name == segment_b_name), None)

                    if segment_a is None or segment_b is None:
                        print(f"Não foi possível encontrar um ou ambos os bairros: {segment_a_name}, {segment_b_name}")
                        continue

                    print(f"Segmento de {segment_a.name} para {segment_b.name} com custo por km de {cost_per_km}")
                    segments.append(Segment(segment_a, segment_b, float(cost_per_km)))

            print("Segmentos carregados com sucesso.")
            return segments
    except Exception as e:
        print(e)
        return []
    
def menu() -> int:
    print("")
    print("Menu")
    print("==========================================")
    print("1. Cadastrar bairro")
    print("2. Cadastrar segmento de rede")
    print("3. Visualizar grafo")
    print("4. Calcular menor caminho para novo segmento de rede")
    print("5. Gerar topologia de rede de custo minimo")
    print("6. Gerar matriz de adjacência")
    print("7. Gerar árvore geradora mínima")
    print("8. Carregar bairros do arquivo")
    print("9. Carregar segmentos do arquivo")
    print("10. Sair")
    print("")
    while True:
        try:
            option = int(input("--- Digite o número da opção escolhida: "))
            if option not in range(1, 11):
                print(INVALID_OPTION)
            else:
                return option
        except ValueError:
            print(INVALID_OPTION)

def register_neighborhood(number_of_neighborhoods: int) -> list:
    neighborhoods = []
    if number_of_neighborhoods <= 0 or not isinstance(number_of_neighborhoods, int):
        print("Número de bairros inválido.")
        return neighborhoods
        
    for _ in range(number_of_neighborhoods):
        name = input("Digite o nome do bairro: ")
        coordenada = input("Digite a latitude e longitude do bairro (separados por vírgula): ")
        latitude, longitude = map(float, coordenada.split(","))
        city = input("Digite a cidade do bairro: ")
        if city == "":
            neighborhoods.append(Neighborhood(name, latitude, longitude))
        else:
            neighborhoods.append(Neighborhood(name, latitude, longitude, city))
    return neighborhoods

def small_way(g, node_a, node_b):
    try:
        graph_nx = nx.Graph()
        for node in g.nodes:
            for neighbor, weight in node.adjacent_nodes.items():
                graph_nx.add_edge(node.neighborhood.name, neighbor.neighborhood.name, weight=weight)

        way = nx.dijkstra_path(graph_nx, node_a.neighborhood.name, node_b.neighborhood.name, weight='weight')
        cost = nx.dijkstra_path_length(graph_nx, node_a.neighborhood.name, node_b.neighborhood.name, weight='weight')
        return way, cost
    except nx.NetworkXNoPath:
        return None, float('inf')

def close_program():
    print("Programa encerrado.")
    exit()


def view_graph_on_map(g : Graph, is_mst=False):
    #O no do grafico deve ter o texto com o nome do bairro
    node_positions = {}
    if not g.nodes:
        print("A lista de nós está vazia.")
        return
    else:
        print("A lista de nós não está vazia.")
    
    for node in g.nodes:
        node_positions[node.neighborhood.name] = (node.neighborhood.longitude, node.neighborhood.latitude)
    
    node_gdf = gpd.GeoDataFrame(
        {'neighborhood': [node.neighborhood.name for node in g.nodes]},
        geometry=[Point(node.neighborhood.longitude, node.neighborhood.latitude) for node in g.nodes],
        crs="EPSG:4326"
    )
    print(f"Subplot: {node_gdf.crs.to_string()}")
    _, ax = plt.subplots(figsize=(20, 20))
    
    # Se is_mst é True, plote os nós
    if is_mst:
        if node_gdf.is_valid.all():
            node_gdf.plot(ax=ax, color='blue')
        else:
            print("Os dados em node_gdf não são válidos.")
        
        

    print(f"Apos plotar os bairros: {node_gdf.crs.to_string()}")
    print(node_gdf.head())
    
    # Plot nodes
    node_gdf.plot(ax=ax, color='blue')
    
    # Plot edges and add edge labels
    for node in g.nodes:
        for neighbor, weight in node.adjacent_nodes.items():
            x_values = [node.neighborhood.longitude, neighbor.neighborhood.longitude]
            y_values = [node.neighborhood.latitude, neighbor.neighborhood.latitude]
            ax.plot(x_values, y_values, color='black')
            mid_x = (x_values[0] + x_values[1]) / 2
            mid_y = (y_values[0] + y_values[1]) / 2
            ax.text(mid_x, mid_y, f'{weight:.2f}', color='red', fontsize=11, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'), zorder=5)

    # Plot node labels
    for node, position in node_positions.items():
        ax.text(position[0], position[1], node, fontsize=10, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'), zorder=5)

    # Add basemap
    ctx.add_basemap(ax, crs=node_gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron)
    
    # Define aspect ratio of y-axis manually if cos_value is not zero
    y_coord = node_gdf.geometry.y.mean()
    print(f"y_coord: {y_coord}")
    cos_value = np.cos(y_coord * np.pi / 180)
    print(f"cos_value: {cos_value}")
    if cos_value != 0:
        ax.set_aspect(1 / cos_value)
    
    plt.show()

def generate_minimum_spanning_tree(g: Graph):
    mst_graph = Graph()
    visited = set()

    # Escolha um nó inicial arbitrário
    start_node = next(iter(g.nodes))

    # Use uma fila de prioridade para armazenar os segmentos com seus custos
    edges = [(0, start_node.name, start_node.name)]

    while edges:
        # Obtenha o segmento de menor custo
        cost, from_node_name, to_node_name = heapq.heappop(edges)
        from_node = g.get_node(from_node_name)
        to_node = g.get_node(to_node_name)

        if to_node_name not in visited:
            visited.add(to_node_name)

            # Adicione os nós ao gráfico da árvore geradora mínima
            mst_graph.add_node(from_node)
            mst_graph.add_node(to_node)

            # Adicione o segmento ao gráfico da árvore geradora mínima
            mst_graph.add_edge(from_node, to_node, cost)
    if not g.nodes:
        print("Nenhum nó foi adicionado ao grafo.")
    else:
        print(f"{len(g.nodes)} nós foram adicionados ao grafo.")
    print(f"MST_GRAPH: {mst_graph.nodes}")
    return mst_graph

def view_mst_on_map(mst_graph):
    view_graph_on_map(mst_graph, is_mst=True)
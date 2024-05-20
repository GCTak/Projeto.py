#encoding: utf-8
import networkx as nx
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point
from classes import Neighborhood, Node, Graph, Segment

def main():
    print("Instalação da rede de internet fibra ótica")
    print("==========================================")
    G = Graph()
    neighborhoods = []
    network_segments = []

    while True:
        choosed_option = menu()

        if choosed_option == 1:
            number_of_neighborhoods = int(input("Digite o número de bairros a serem cadastrados: "))
            neighborhoods = register_neighborhood(number_of_neighborhoods)
            for neighborhood in neighborhoods:
                G.add_node(Node(neighborhood))

        elif choosed_option == 2:
            segmentA_name = input("Digite o nome do bairro de origem: ")
            segmentB_name = input("Digite o nome do bairro de destino: ")
            cost_per_km = input("Digite o custo por km do segmento de rede: ")
            if not cost_per_km:
                cost_per_km = 1
            
            
            
            segmentA = next((neighborhood for neighborhood in neighborhoods if neighborhood.name == segmentA_name), None)
            segmentB = next((neighborhood for neighborhood in neighborhoods if neighborhood.name == segmentB_name), None)
            
            if segmentA and segmentB:
                segment = Segment(segmentA, segmentB, cost_per_km)
                network_segments.append(segment)
                nodeA = next(node for node in G.nodes if node.neighborhood.name == segmentA_name)
                nodeB = next(node for node in G.nodes if node.neighborhood.name == segmentB_name)
                G.add_edge(nodeA, nodeB, segment.weight)
            else:
                print("Um ou ambos os bairros não foram encontrados.")

        elif choosed_option == 3:
            view_graph_on_map(G)

        elif choosed_option == 4:
            segmentA_name = input('Digite o nome do bairro de origem:\n')
            segmentB_name = input('Digite o nome do bairro de destino:\n')
            nodeA = next((node for node in G.nodes if node.neighborhood.name == segmentA_name), None)
            nodeB = next((node for node in G.nodes if node.neighborhood.name == segmentB_name), None)
            
            if nodeA and nodeB:
                way, cost = small_way(G, nodeA, nodeB)
                if way:
                    print(f'O caminho de custo mínimo de {segmentA_name} para {segmentB_name} é: {way}')
                    print(f'O custo desse caminho é: {cost} milhões de reais')
                else:
                    print(f'Não há caminho disponível de {segmentA_name} para {segmentB_name}')
            else:
                print("Um ou ambos os bairros não foram encontrados.")

        elif choosed_option == 5:
            pass

        elif choosed_option == 6:
            node_names, adjacency_matrix = G.adjacent_matrix()
            print("Matriz de Adjacência:")
            print("  " + " ".join(node_names))
            for name, row in zip(node_names, adjacency_matrix):
                print(f"{name} {' '.join(map(str, row))}")

        elif choosed_option == 7:
            pass

        elif choosed_option == 8:
            close_program()

        else:
            print("Opção inválida")
            continue

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
    print("8. Sair")
    print("")
    while True:
        try:
            option = int(input("--- Digite o número da opção escolhida: "))
            if option not in range(1, 9):
                print("Opção inválida")
            else:
                return option
        except ValueError:
            print("Opção inválida")

def register_neighborhood(number_of_neighborhoods: int) -> list:
    neighborhoods = []
    if number_of_neighborhoods <= 0 or not isinstance(number_of_neighborhoods, int):
        print("Número de bairros inválido.")
        return neighborhoods
        
    for i in range(number_of_neighborhoods):
        name = input("Digite o nome do bairro: ")
        coordenada = input("Digite a latitude e longitude do bairro (separados por vírgula): ")
        latitude, longitude = map(float, coordenada.split(","))
        city = input("Digite a cidade do bairro: ")
        if city == "":
            neighborhoods.append(Neighborhood(name, latitude, longitude))
        else:
            neighborhoods.append(Neighborhood(name, latitude, longitude, city))
    return neighborhoods

def small_way(G, nodeA, nodeB):
    try:
        node_dict = {node.neighborhood.name: node for node in G.nodes}
        graph_nx = nx.Graph()
        for node in G.nodes:
            for neighbor, weight in node.adjacent_nodes.items():
                graph_nx.add_edge(node.neighborhood.name, neighbor.neighborhood.name, weight=weight)

        way = nx.dijkstra_path(graph_nx, nodeA.neighborhood.name, nodeB.neighborhood.name, weight='weight')
        cost = nx.dijkstra_path_length(graph_nx, nodeA.neighborhood.name, nodeB.neighborhood.name, weight='weight')
        return way, cost
    except nx.NetworkXNoPath:
        return None, float('inf')

def close_program():
    print("Programa encerrado.")
    exit()

def view_graph_on_map(G):
    #O no do grafico deve ter o texto com o nome do bairro
    node_positions = {}
    for node in G.nodes:
        node_positions[node.neighborhood.name] = (node.neighborhood.longitude, node.neighborhood.latitude)
    
    node_gdf = gpd.GeoDataFrame(
        {'neighborhood': [node.neighborhood.name for node in G.nodes]},
        geometry=[Point(node.neighborhood.longitude, node.neighborhood.latitude) for node in G.nodes],
        crs="EPSG:4326"
    )

    fig, ax = plt.subplots(figsize=(20, 20))

    # Plot nodes
    node_gdf.plot(ax=ax, color='blue')

    # Plot edges and add edge labels
    for node in G.nodes:
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

    
    
    
    plt.show()

if __name__ == "__main__":
    main()

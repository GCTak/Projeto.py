#encoding: utf-8
from classes import Neighborhood, Node, Graph, Segment
from functions import *
from tabulate import tabulate

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
            segment_a_name = input("Digite o nome do bairro de origem: ")
            segment_b_name = input("Digite o nome do bairro de destino: ")
            cost_per_km = input("Digite o custo por km do segmento de rede: ")
            if not cost_per_km:
                cost_per_km = 1
            else:
                cost_per_km = float(cost_per_km)
            
            segment_a = next((neighborhood for neighborhood in neighborhoods if neighborhood.name == segment_a_name), None)
            segment_b = next((neighborhood for neighborhood in neighborhoods if neighborhood.name == segment_b_name), None)
            
            if segment_a and segment_b:
                segment = Segment(segment_a, segment_b, cost_per_km)
                network_segments.append(segment)
                node_a = next(node for node in G.nodes if node.neighborhood.name == segment_a_name)
                node_b = next(node for node in G.nodes if node.neighborhood.name == segment_b_name)
                G.add_edge(node_a, node_b, segment.weight)
            else:
                print("Um ou ambos os bairros não foram encontrados.")

        elif choosed_option == 3:
            view_graph_on_map(G)

        elif choosed_option == 4:
            segment_a_name = input('Digite o nome do bairro de origem:\n')
            segment_b_name = input('Digite o nome do bairro de destino:\n')
            cost_per_km = input('Digite o custo por km do segmento de rede:\n')
            if not cost_per_km or cost_per_km == '':
                cost_per_km = 1
            else:
                cost_per_km = float(cost_per_km)
            node_a = next((node for node in G.nodes if node.neighborhood.name == segment_a_name), None)
            node_b = next((node for node in G.nodes if node.neighborhood.name == segment_b_name), None)
            
            if node_a and node_b:
                way, cost = small_way(G, node_a, node_b)
                if way:
                    print(f'O caminho de custo mínimo de {segment_a_name} para {segment_b_name} é: {way}')
                    print(f'O custo desse caminho é: {cost*cost_per_km} milhões de reais')
                else:
                    print(f'Não há caminho disponível de {segment_a_name} para {segment_b_name}')
            else:
                print("Um ou ambos os bairros não foram encontrados.")

        elif choosed_option == 5:
            mst_graph = generate_minimum_spanning_tree(G)
            print("Topologia de rede de custo mínimo gerada com sucesso.")
            view_mst_on_map(mst_graph)
            
        elif choosed_option == 6:
            node_names, adjacency_matrix = G.adjacent_matrix()
            print("Matriz de Adjacência:")
            table = [ [name] + row for name, row in zip(node_names, adjacency_matrix) ]
            print(tabulate(table, headers=[""] + node_names, tablefmt="pretty"))

        elif choosed_option == 7:
            mst = generate_mst(G)
            view_graph(mst)
            


        elif choosed_option == 8:
            loaded_neighborhoods = load_neighborhoods()
            if loaded_neighborhoods is not None or loaded_neighborhoods != [] or loaded_neighborhoods != False:
                print("Bairros carregados com sucesso.")
                neighborhoods = loaded_neighborhoods
                for neighborhood in neighborhoods:
                    G.add_node(Node(neighborhood))
            else:
                print("Não foi possível carregar os bairros do arquivo.")

        elif choosed_option == 9:
            # Carregue os bairros primeiro
            neighborhoods = load_neighborhoods()
            if neighborhoods is not False:
                # Agora passe os bairros para a função load_segments
                loaded_segments = load_segments(neighborhoods)
                if loaded_segments is not None and loaded_segments != [] and loaded_segments != False:
                    print("Segmentos de rede carregados com sucesso.")
                    network_segments = loaded_segments
                    for segment in network_segments:
                        segment_a = next(node for node in G.nodes if node.neighborhood.name == segment.segment_a.name)
                        segment_b = next(node for node in G.nodes if node.neighborhood.name == segment.segment_b.name)
                        G.add_edge(segment_a, segment_b, segment.weight)
                else:
                    print("Não foi possível carregar os segmentos de rede do arquivo.")
        
        elif choosed_option == 10:
            close_program()

        else:
            print(INVALID_OPTION)


if __name__ == "__main__":
    main()

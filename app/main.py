#encoding: utf-8
import networkx as nx
import matplotlib.pyplot as plt
from classes import Neighborhood

def main():
    print(f"Instalação da rede de internet fibra ótica")
    print(f"==========================================")
    while True:
        choosed_option = menu()
        neighboorhoods = []
        network_segments = []
        G = nx.Graph()

        if choosed_option == 1:
            number_of_neighboorhoods = int(input("Digite o número de bairros a serem cadastrados: "))
            neighboorhoods = register_neighborhood(number_of_neighboorhoods)

        elif choosed_option == 2:
            segmentA = input("Digite o nome do bairro de origem: ")
            segmentB = input("Digite o nome do bairro de destino: ")
            weight = float(input("Digite o custo do segmento de rede: "))
            network_segments.append(register_network_segment(segmentA, segmentB, weight))

        elif choosed_option == 3:
            for segment in network_segments:
                segmentA, segmentB, weight = segment
                G.add_edge(segmentA, segmentB, weight=weight)
            
            pos = nx.spring_layout(G)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            view_graph(G, pos, edge_labels)

        elif choosed_option == 4:
            segmentA = input('Digite o nome do bairro de origem:\n')
            segmentB = input('Digite o nome do bairro de destino:\n')
            way, cost = small_way(G, segmentA, segmentB)
            if way:
                print(f'O caminho de custo mínimo de {segmentA} para {segmentB} é: {way}')
                print(f'O custo desse caminho é: {cost} milhões de reais')
            else:
                print(f'Não há caminho disponível de {segmentA} para {segmentB}')

        elif choosed_option == 5:
            pass

        elif choosed_option == 6:
            pass

        elif choosed_option == 7:
            pass

        elif choosed_option == 8:
            close_program()

        else:
            print(f"Opção inválida")
            continue

def menu() -> int:
    print(f"")
    print(f"Menu")
    print(f"==========================================")
    print(f"1. Cadastrar bairro")
    print(f"2. Cadastrar segmento de rede")
    print(f"3. Visualizar grafo")
    print(f"4. Calcular menor caminho para novo segmento de rede")
    print(f"5. Gerar topologia de rede de custo minimo")
    print(f"6. Gerar matriz de adjacência")
    print(f"7. Gerar árvore geradora mínima")
    print(f"8. Sair")
    print(f"")
    while True:
        try:
            option = int(input("--- Digite o número da opção escolhida: "))
            if option not in range(1, 9):
                print(f"Opção inválida")
            else:
                return option
        except ValueError:
            print(f"Opção inválida")


def register_neighborhood(number_of_neighboorhoods: int) -> list:
    neighboorhoods = []
    if number_of_neighboorhoods <= 0 or not isinstance(number_of_neighboorhoods, int):
        print(f"Número de bairros inválido.")
        return neighboorhoods
        
    for i in range(number_of_neighboorhoods):
        name = input("Digite o nome do bairro: ")
        coordenada = input("Digite a latitude e longitude do bairro (separados por vírgula): ")
        latitude, longitude = coordenada.split(",")
        latitude = float(latitude)
        longitude = float(longitude)
        city = input("Digite a cidade do bairro: ")
        if city == "":
            neighboorhoods.append(Neighborhood(name, latitude, longitude))
        else:
            neighboorhoods.append(Neighborhood(name, latitude, longitude, city))
    return neighboorhoods

def register_network_segment(segmentA: str, segmentB: str, weight: float) -> tuple:
    return (segmentA, segmentB, {'weight': weight})

def view_graph(G, pos, edge_labels):
    try:
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=1000,
            node_color='lightblue',
            font_weight='bold',
            arrowsize=20
        )
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            label_pos=0.5,  
            font_size=10,   
            font_color='red' 
        )
        plt.show()
    except Exception as e:
        print(f"Erro ao gerar a visualização do grafo: {e}")

def small_way(G, segmentA , segmentB):
    try:
        way = nx.dijkstra_path(G, segmentA, segmentB, weight='weight')
        cost = nx.dijkstra_path_length(G, segmentA, segmentB, weight='weight')
        return way, cost
    except nx.NetworkXNoPath:
        return None, float('inf')
    
def close_program():
    print(f"Programa encerrado.")
    exit()

if __name__ == "__main__":
    main()
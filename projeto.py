import networkx as nx
import matplotlib.pyplot as plt

#Função para criar o grafo
def grafo():

    # Definindo o Grafo
    G = nx.Graph()

    # Definindo os vértices (bairros)
    bairros = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    # Adicionando arestas direcionadas (segmentos de rede) e seus pesos (custos)
    # segmentos_de_rede = [(Bairro Origem, Bairro Destino, Custo)]
    segmentos_de_rede = [
        ('A', 'B', {'weight': 7}),
        ('A', 'C', {'weight': 5}),
        ('A', 'D', {'weight': 5.5}),
        ('B', 'D', {'weight': 7.5}),
        ('B', 'E', {'weight': 8}),
        ('C', 'D', {'weight': 6}),
        ('C', 'F', {'weight': 6.5}),
        ('D', 'F', {'weight': 5.5}),
        ('D', 'G', {'weight': 3.5}),
        ('D', 'H', {'weight': 6.5}),
        ('E', 'G', {'weight': 4}),
        ('E', 'I', {'weight': 5}),
        ('F', 'H', {'weight': 5}),
        ('G', 'H', {'weight': 5}),
        ('G', 'I', {'weight': 5}),
        ('H', 'J', {'weight': 7.5}),
        ('I', 'J', {'weight': 5.5}),
    ]

    G.add_edges_from(segmentos_de_rede)

    return G

# Função para visualizar o grafo
def visualizacao_grafo(G, pos, edge_labels):
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

# Função para cadastrar os bairros
def cadastrar_bairros(G):
    bairros = input('Digite o nome do novo bairro: ')
    G.add_nodes_from(bairros)

# Função principal
def main():
    G = grafo()
    while True:
        print('\nEscolha uma operação:')
        print('1. Cadastrar novo bairro')
        print('2. Cadastrar custos de construção dos segmentos entre bairros vizinhos')
        print('3. Visualizar o grafo')
        print('4. Sair')
        escolha = input('Digite o número da operação desejada: ')
        
        if escolha == '1':
            cadastrar_bairros(G)

if __name__ == "__main__":
    main()
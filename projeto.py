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

# Função principal
def main():

    # Definindo o grafo
    G = grafo()  

    #Passando os parâmetros da função visualizacao_grafo
    pos = nx.spring_layout(G)  
    edge_labels = nx.get_edge_attributes(G, 'weight')  
    
    # Executando a função visualizacao_grafo
    visualizacao_grafo(G, pos, edge_labels) 

if __name__ == "__main__":
    main()

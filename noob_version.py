import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import deque

# Função para criar o grafo
def grafo(segmentos_de_rede):
    G = nx.Graph()
    G.add_edges_from(segmentos_de_rede)
    return G

# Função para visualizar o grafo
def visualizacao_grafo(G, pos=None, edge_labels=None):
    if pos is None:
        pos = nx.spring_layout(G)
    if edge_labels is None:
        edge_labels = nx.get_edge_attributes(G, 'weight')

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

def bfs_caminho_custo_minimo(G, origem, destino):

    # Inicializa uma fila para a busca em largura
    fila = deque([(origem, [origem])])

    # Enquanto houver vértices na fila
    while fila:
        vertice, caminho = fila.popleft()

        # Se alcançamos o destino, retornamos o caminho
        if vertice == destino:
            custo = calcular_custo_caminho(G, caminho)
            return caminho, custo

        # Para cada vértice adjacente ao vértice atual
        for vizinho in G[vertice]:
            # Adiciona o vértice adjacente à fila com o caminho atualizado
            if vizinho not in caminho:
                fila.append((vizinho, caminho + [vizinho]))

    # Se não encontrarmos um caminho, retorna None
    return None, float('inf')

def calcular_custo_caminho(G, caminho):
    # Calcula o custo total do caminho
    custo_total = 0
    for i in range(len(caminho) - 1):
        vertice_atual = caminho[i]
        proximo_vertice = caminho[i + 1]
        custo_total += G[vertice_atual][proximo_vertice]['weight']
    return custo_total

# Função para calcular o caminho de custo mínimo
def caminho_custo_minimo_dijkstra(G, origem, destino):
    try:
        caminho = nx.dijkstra_path(G, origem, destino, weight='weight')
        custo = nx.dijkstra_path_length(G, origem, destino, weight='weight')
        return caminho, custo
    except nx.NetworkXNoPath:
        return None, float('inf')

# Função para criar a matriz de adjacência
def criar_matriz_adjacencia(segmentos_de_rede):
    bairros = list(set(sum(([a, b] for a, b, _ in segmentos_de_rede), [])))
    num_bairros = len(bairros)
    matriz_adj = [[0] * num_bairros for _ in range(num_bairros)]

    for origem, destino, dados in segmentos_de_rede:
        i = bairros.index(origem)
        j = bairros.index(destino)
        custo = dados['weight']
        matriz_adj[i][j] = custo
        matriz_adj[j][i] = custo

    return matriz_adj, bairros

# Função para imprimir a matriz de adjacência
def print_matriz_adjacencia(matriz_adj, bairros):
    df = pd.DataFrame(matriz_adj, index=bairros, columns=bairros)
    print(df)

# Função para calcular o custo de construção de todos os segmentos de rede
def calcular_custo_total(segmentos_de_rede):
    return sum(dados['weight'] for _, _, dados in segmentos_de_rede)

# Função para encontrar a Árvore Geradora Mínima usando o algoritmo de Kruskal
def arvore_geradora_minima(G):
    AGM = nx.minimum_spanning_tree(G, algorithm='kruskal')
    return AGM

# Função para permitir que o usuário escolha entre as operações
def menu(bairros, segmentos_de_rede, G):

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    continuar = 'sim'

    while continuar == 'sim':
        print('MENU DE OPERAÇÕES')
        print('1. Cadastro de bairro')
        print('2. Cadastro do custo de segmentos de redes')
        print('3. Caminho de custo mínimo')
        print('4. Caminho de custo mínimo - Dijkstra')
        print('5. Visualizar grafo')
        print('6. Visualizar matriz de adjacência')
        print('7. Calcular custo total da construção')
        print('8. Topologia de rede de custo mínimo')
        print('0. Sair do menu')

        escolha = int(input('Qual operação você gostaria de fazer?\n'))

        if escolha == 1:
            novo_bairro = input('Digite o nome do bairro a ser cadastrado: \n')
            bairros.append(novo_bairro)
            G.add_node(novo_bairro)
            print('Bairro cadastrado com sucesso')
        elif escolha == 2:
            bairro_origem = input('Qual será o bairro origem? \n')
            bairro_destino = input('Qual será o bairro destino? \n')
            custo = float(input('Qual será o custo? \n'))
            segmentos_de_rede.append((bairro_origem, bairro_destino, {'weight': custo}))
            G.add_edge(bairro_origem, bairro_destino, weight=custo)
            print('Custo de segmento de rede cadastrado com sucesso!')
        elif escolha == 3:
            origem = input('Qual será o bairro origem?\n')
            destino = input('Qual será o bairro destino?\n')
            caminho, custo = bfs_caminho_custo_minimo(G, origem, destino)
            if caminho:
                print(f'O caminho de custo mínimo de {origem} para {destino} é: {caminho}')
                print(f'O custo desse caminho é: {custo} milhões de reais')
            else:
                print(f'Não há caminho disponível de {origem} para {destino}')
        elif escolha == 4:
            origem = input('Qual será o bairro origem?\n')
            destino = input('Qual será o bairro destino?\n')
            caminho, custo = caminho_custo_minimo_dijkstra(G, origem, destino)
            if caminho:
                print(f'O caminho de custo mínimo de {origem} para {destino} é: {caminho}')
                print(f'O custo desse caminho é: {custo} milhões de reais')
            else:
                print(f'Não há caminho disponível de {origem} para {destino}')
        elif escolha == 5:
            visualizacao_grafo(G, pos, edge_labels)
        elif escolha == 6:
            matriz_adj, bairros = criar_matriz_adjacencia(segmentos_de_rede)
            print('\nMatriz de adjacência:')
            print_matriz_adjacencia(matriz_adj, bairros)
        elif escolha == 7:
            custo_total = calcular_custo_total(segmentos_de_rede)
            print(f'Caso todos os segmentos fossem construídos o custo total para a construção da infraestrutura é de {custo_total} milhões de reais')
        elif escolha == 8:
            AGM = arvore_geradora_minima(G)
            custo_total_AGM = calcular_custo_total(list(AGM.edges(data=True)))
            print('Topologia de rede de custo mínimo (Árvore Geradora Mínima):')
            print(list(AGM.edges(data=True)))
            print(f'O custo total da árvore geradora mínima é: {custo_total_AGM} milhões de reais')
            visualizacao_grafo(AGM)
        elif escolha == 0:
            print('Saindo do menu...')
            break
        else:
            print('Operação não disponível')

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        resposta = input('Gostaria de usar outra operação? (sim/não)\n').lower()
        continuar = resposta

    return bairros, segmentos_de_rede, G

# Função principal
def main():
    bairros = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

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

    # Definindo o grafo
    G = grafo(segmentos_de_rede)

    # Executando a função do menu de operações
    bairros, segmentos_de_rede, G = menu(bairros, segmentos_de_rede, G)

if __name__ == "__main__":
    main()
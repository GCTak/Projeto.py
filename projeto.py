import networkx as nx
import matplotlib.pyplot as plt

#Função para criar o grafo
def grafo(segmentos_de_rede):

    # Definindo o Grafo
    G = nx.Graph()

    # Adição das arestas ao grafo 'G' definido acima
    G.add_edges_from(segmentos_de_rede)

    # Retornando o grafo para utilizar em outras funções
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

# Função para permitir que o usuário escolha entre as operações
def menu(bairros, segmentos_de_rede, G, pos, edge_labels):

    continuar = True

    while continuar:
        # Apresentando o menu
        print('MENU DE OPERAÇÕES')
        print('1. Cadastro de bairro')
        print('2. Cadastro do custo de segmentos de redes')

        # Preparando o programa para receber a escolha do usuário sobre qual operação ele deseja realizar
        escolha = int(input('Qual operação você gostaria de fazer?\n'))

        # Verificação de qual operação o usuário escolheu com base na variável 'escolha'
        if escolha == 1:
            novo_bairro = input('Digite o nome do bairro a ser cadastrado: \n')
            bairros.append(novo_bairro)
            G.add_node(novo_bairro)  # Adicionando o novo bairro ao grafo
            print('Bairro cadastrado com sucesso')
        elif escolha == 2:
            bairro_origem = input('Qual será o bairro origem? \n')
            bairro_destino = input('Qual será o bairro destino? \n')
            custo = input('Qual será o custo? \n')
            segmentos_de_rede.append((bairro_origem, bairro_destino, {'weight': float(custo)}))
            G.add_edge(bairro_origem, bairro_destino, weight=float(custo))  # Adicionando o novo segmento de rede ao grafo
            print('Custo de segmento de rede cadastrado com sucesso!')
        else: 
            print('Operação não disponível')

        # Perguntar ao usuário se ele deseja continuar
        resposta = input('Gostaria de usar outra operação? (sim/não)\n')
        continuar = resposta.lower() == 'sim'

        # Após qualquer modificação no grafo, o layout do grafo será atualizado
        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')

        return pos, edge_labels

# Função principal
def main():

    # Definindo a lista de bairros globalmente
    bairros = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    # Definindo as arestas direcionadas (segmentos de rede) e seus pesos (custos) globalmente
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

    # Passando os parâmetros da função visualizacao_grafo
    pos = nx.spring_layout(G)  
    edge_labels = nx.get_edge_attributes(G, 'weight')  
    
    # Executando a função visualizacao_grafo
    visualizacao_grafo(G, pos, edge_labels) 

    # Executando o menu de opções
    menu(bairros, segmentos_de_rede, G, pos, edge_labels)

    # Atualizando o grafo com os novos segmentos de rede
    G = grafo(segmentos_de_rede)

    # Executando o menu de opções e obtendo o layout e os rótulos das arestas atualizados
    pos, edge_labels = menu(bairros, segmentos_de_rede, G, pos, edge_labels)

    # Visualizando o grafo atualizado
    visualizacao_grafo(G, pos, edge_labels)

if __name__ == "__main__":
    main()
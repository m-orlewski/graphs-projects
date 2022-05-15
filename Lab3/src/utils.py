import networkx as nx
import random


def check_sequence(sequence):
    '''Sprawdza czy podana sekwencja jest ciągiem graficznym'''
    sequence.sort(reverse=True)
    n = len(sequence)
    
    while True:
        if all(i == 0 for i in sequence):
            return True

        if sequence[0] < 0 or sequence[0] >= n or any(i < 0 for i in sequence[1:n]):
            return False

        for i in range(1, sequence[0] + 1):
            sequence[i] -= 1

        sequence[0] = 0
        sequence.sort(reverse=True)

def create_graph_from_sequence(sequence):
    '''Tworzy graf z podanej sekwencji graficznej'''
    sequence.sort(reverse=True)
    n = len(sequence)
    g = nx.Graph()

    d = [] # [numer wierzchołka, liczba sąsiadów]
    for i in range(n):
        d.append([i+1, sequence[i]])

    g.add_nodes_from([i[0] for i in d]) # dodajemy wierzchołki do grafu

    while not all(i[1] == 0 for i in d): # dopóki sekwencja nie składa się z zer
        node = d[0][0] # numer wierzchołka o największej liczbie sąsiadów
        edges = d[0][1] # liczba sąsiadów
        for i in range(edges):
            g.add_edge(node, d[i+1][0], weight = random.randint(1,10)) # dodajemy krawędzie między wierzchołkiem node a kolejnymi wierzchołkami wraz z ich wagami
            d[i+1][1] -= 1 # zmniejszamy liczbę sąsiadów dla kolejnych wierzchołków połączonych z node

        d[0][1] = 0 # zerujemy liczbę sąsiadów dla wierzchołka node
        d.sort(key=lambda x: x[1], reverse=True) # sortujemy listę wierzchołków po liczbie sąsiadów nierosnąco

    while not nx.is_connected(g): # ta część tworzy graf spójny petla dopóki graf nie będzie spójny
        list_of_comps = list(nx.connected_components(g)) #zwraca liste komponentów coś na zasadzie comps z lab2
        random_node1 = random.sample(list_of_comps[1], 1)[0] #losuje wezeł z jednej grupy
        random_node2 = random.sample(list_of_comps[0], 1)[0] #losuje wezeł z drugiej grupy 
        g.add_edge(random_node1, random_node2, weight = random.randint(1,10)) #dodaje krawędz z wagą pomiędzy nimi
    return g

if __name__ == '__main__':
    print(check_sequence([4,2,2,3,2,1,4,2,2,2,2]))
    a = create_graph_from_sequence([4,2,2,3,2,1,4,2,2,2,2])
    print(a.edges)
    print(nx.is_connected(a))

    
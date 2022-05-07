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
            g.add_edge(node, d[i+1][0]) # dodajemy krawędzie między wierzchołkiem node a kolejnymi wierzchołkami
            d[i+1][1] -= 1 # zmniejszamy liczbę sąsiadów dla kolejnych wierzchołków połączonych z node

        d[0][1] = 0 # zerujemy liczbę sąsiadów dla wierzchołka node
        d.sort(key=lambda x: x[1], reverse=True) # sortujemy listę wierzchołków po liczbie sąsiadów nierosnąco
    
    return g

def randomize_graph(g, count):
    '''Randomizuje graf zamieniając count razy losową parę krawędzi ab i cd na ad i bc'''
    edges = list(g.edges)
    for i in range(len(edges)):
        edges[i] = list(edges[i]) # tuples -> lists


    for _ in range(count):
        [i, j] = random.sample(range(len(edges)), 2) # losujemy 2 krawędzie

        b = edges[i][1]
        c = edges[j][0]
        d = edges[j][1]

        edges[i][1] = d
        edges[j][0] = b 
        edges[j][1] = c

    return nx.Graph(edges)


if __name__ == '__main__':
    print(check_sequence([3,2,3,2,2]))
    create_graph_from_sequence([3,2,3,2,2])

    print(check_sequence([4,2,2,3,2,1,4,2,2,2,2]))
    create_graph_from_sequence([4,2,2,3,2,1,4,2,2,2,2])

    randomize_graph(create_graph_from_sequence([3,2,3,2,2]), 2)
    
        
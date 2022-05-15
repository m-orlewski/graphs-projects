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

def rand_change_edge(edges):

    [i, j] = random.sample(range(len(edges)), 2) # losujemy 2 krawędzie
    e1=edges[i].copy()
    e2=edges[j].copy()
    e1[1]=edges[j][1]
    e2[0]=edges[i][1]
    e2[1]=edges[j][0]

    l=0

    while e1 in edges or e2 in edges or [e1[1],e1[0]] in edges or [e2[1],e2[0]] in edges or e1[0]==e1[1] or e2[0]==e2[1]: #Powtarzamy losowanie dopóki nowe krawedzie nie będą duplikatami starych lub petlami na danym wierzcholku
        [i, j] = random.sample(range(len(edges)), 2) 
        e1=edges[i].copy()
        e2=edges[j].copy()
        e1[1]=edges[j][1]
        e2[0]=edges[i][1]
        e2[1]=edges[j][0]
        l=l+1
        if l==200:
            break

    edges[i]=e1
    edges[j]=e2

def randomize_graph(g, count):
    '''Randomizuje graf zamieniając count razy losową parę krawędzi ab i cd na ad i bc'''
    edges = list(g.edges)
    for i in range(len(edges)):
        edges[i] = list(edges[i]) # tuples -> lists

    for i in range(count):
        rand_change_edge(edges) # wywołanie funkcji zamieniającej dwie krawędzie

    return nx.Graph(edges)


def components_R(nr, node, g, comp):
    for nbr in g[node]: #Przeglądam wszystkich sąsiadów danego węzła
        if comp[nbr] == -1: #jeżeli sąsiad nie był odwiedzony przypisuje mu wartość odpowiedniej grupy
            comp[nbr] = nr
            components_R(nr, nbr, g, comp) #przeszkuję w głąb sąsiadów sąsiada

def components(g):
    nr = 0
    comp = {} #Tworze słownik key: idex węzła value: grupa do której przynależy
    for node in g:
        comp[node] = -1 #Zgodnie z algorytmem przypisuje każdemu kluczowi wartość -1
    for node in g:
        if comp[node] == -1: #sprawdzam czy węzeł był odwiedzony -1 -> nie był każda inna był
            nr = nr+1 #nowa grupa
            comp[node] = nr #przypisuje do noda do której grupy przynależy
            components_R(nr, node, g, comp) #Przeszukiwanie w głab po każdym sąsiedzie węzła 
                                    #  nr -> numer grupy, node -> aktualny węzeł, g->Oryginalny graf, comp->słownik z przynależnością
    return comp

def generate_random_k_regular(k,n=None):
    repeat=False
    if n==None:
        n=random.randrange(2,100) #Losowanie wartości n jeśli nie podana
        repeat=True

    seq=[k for _ in range(n)] #Tworzenie sekwancji dla grafu k-regularnego.
    if(check_sequence(seq.copy())): #sprawdzenie czy seqwencja jest poprawna
        graf=create_graph_from_sequence(seq)
        n=len(graf.edges())
        graf=randomize_graph(graf,100) #randomizowanie grafu
        l=0
        while n!=len(graf.edges()):
            graf=create_graph_from_sequence(seq)
            graf=randomize_graph(graf,100) #randomizowanie grafu
            l=l+1
            if(l==200):
                break
        return graf
    else:
        if repeat:
            generate_random_k_regular(k)
        else:
            return None

def try_next_Hamilton(graf,route,nodes): #Funkcja Rekurencyjna do szukania Hamiltona
    w=False # Wynik
    for n in list(graf[route[-1]]): #Przejscie po wierzchołkach od bierzącego wierzchołka
        if n not in route: #jesli wierzchołka nie ma w drodze
            route.append(n) #dodjemy nowy wierzchołek do drogi
            if len(route)==nodes and route[0] in list(graf[route[-1]]): #jesli mamy wszyszskie wierzchołki w drodze sprawdzamy czy możemy dodać wierzchołek startowy jak tk jest to graf Hamiltonowski
                route.append(route[0])
                return True
            w=try_next_Hamilton(graf,route,nodes) #Wywołujemy sprawdzanie wybranego wierzchołka
            if w:
                return True 
            else:
                route.pop() #Usuwamy ostatni elemant drogi
            
    return False
    
def isHamilton(graf): #Funkcja sprawdzająca czy graf jest Hamiltonowski i zwracająca droge
    if set(components(graf).values()) != {1}: #Sprawdzenie czy jest spójny
        return (False,None)
    nodes=len(graf) #Ilość wierzchołków grafu
    route=[1] #Stos do wyznaczanje drogi
    return [try_next_Hamilton(graf,route,nodes),route] #Wywołanie rekurancji do szukania Hamiltona

def generate_random_euler_graph(vertices_amount):
    while True:
        sequence = [random.randrange(2, vertices_amount, 2) for _ in range(vertices_amount)]

        if check_sequence(sequence.copy()):
            return create_graph_from_sequence(sequence)

def find_euler_cycle(graph):
    graph_copy = nx.Graph(graph)
    print(graph_copy.edges)
    cycle = []

    v = list(graph_copy.nodes)[0]
    cycle.append(v)
    while True:
        neighbors = list(graph_copy.adj[v])
        if len(neighbors) == 0:
            break
        elif len(neighbors) == 1:
            u = neighbors[0]
            cycle.append(u)
            graph_copy.remove_edge(v, u)
            v = u
        else:
            for u in neighbors:
                if is_bridge(graph_copy, u, v):
                    continue
                else:
                    cycle.append(u)
                    graph_copy.remove_edge(v, u)
                    v = u
                    break

    return cycle

def is_bridge(graph, u, v):
    components_before = list(nx.connected_components(graph))
    graph.remove_edge(u, v)
    components_after = list(nx.connected_components(graph))
    graph.add_edge(u, v)

    return True if len(components_before) != len(components_after) else False

def nx_graph_to_representation(graph):
    representation = {}

    for node in graph.nodes:
        representation[node] = list(graph.adj[node])

    return dict(sorted(representation.items(), key=lambda x: x[0]))

if __name__ == '__main__':
    print(check_sequence([3,2,3,2,2]))
    create_graph_from_sequence([3,2,3,2,2])

    print(check_sequence([4,2,2,3,2,1,4,2,2,2,2]))
    create_graph_from_sequence([4,2,2,3,2,1,4,2,2,2,2])

    print(check_sequence([2,2,2,2,2,2]))
    if check_sequence([2,2,2,2,2,2]):
        create_graph_from_sequence([2,2,2,2,2,2])

    randomize_graph(create_graph_from_sequence([3,2,3,2,2,5,5,5,5,5,5,4]), 100)
    
    components(create_graph_from_sequence([2,2,2,2,2,2]))

    generate_random_k_regular(4)

    print(isHamilton(generate_random_k_regular(2,8)))
    print(isHamilton(randomize_graph(create_graph_from_sequence([3,2,3,2,2,5,5,5,5,5,5,4]),10)))

    print(generate_random_euler_graph(6).edges)
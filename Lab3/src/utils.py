import networkx as nx
import random
import sys


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

def init(G, s): 
    nx.set_node_attributes(G, sys.maxsize, 'cost') #ustawiam koszt dotarcia do węzła jako inf
    nx.set_node_attributes(G, None, 'prev') #ustawiam poprzednika na nieistenijącego
    G.nodes[s]['cost'] = 0 #ustawiam koszt dotarcia do wezła startowego jako 0 i jego poprzednika jako null

def relax(G, prev_node, current_node):
    if G.nodes[current_node]['cost'] > G.nodes[prev_node]['cost'] + G[prev_node][current_node]['weight']: #jezeli koszt dotarcia do wezla jest wiekszy niz koszt dotarcia do poprzednika + waga krawedzi miedzy nimi
        G.nodes[current_node]['cost'] = G.nodes[prev_node]['cost'] + G[prev_node][current_node]['weight'] # to ustawiam koszt dotarcia do konkretnego wezla jako suma kosztow
        G.nodes[current_node]['prev'] = prev_node #ustawiam poprzednika

def dijkstra(G,s): #G graf, s startowy wezel
    init(G,s) #inicjalizujemy graf dodajemy potrzebne pola cost -> koszt dotarcia, prev -> poprzedni wezeł
    S = [] #lista odwiedzonych węzłów
    while sorted(S) != sorted(G.nodes): #dopóki odwiedzone węzły != wszystkim węzłom to liczymy koszta 
        current_node = min(list(filter(lambda x: x[0] not in S, G.nodes.data('cost'))), key = lambda t: t[1]) #wybieramy wezel spośród nieodwiedzonych który ma najmniejszy koszt dotarcia
        S.append(current_node[0]) #dodajemy takowy do odwiedzonych węzłów --->current_node => (numer węzła, koszt dotarcia) <---
        not_visited = list(filter(lambda x: x not in S, G.neighbors(current_node[0]))) # lista nieodwiedzonych sąsiadów current_node
        for node in not_visited: #petla po nieodwiedzonych sąsiadach
            relax(G, current_node[0], node) #relaksujemy koszty dotarcia i ustawiamy poprzeników dla sasiadów current_node
    #print_graph_paths(G,s) # do wyświetlania, nic specjalnego

def print_graph_paths(G,s): #wyswietla sciezki oraz koszty dotarcia do grafu G graf, s startowy wezeł
    string = ""
    p = []
    for node in G:
        n = node
        string+=f"1 -> {n} ==> {G.nodes[n]['cost']} Path: "
        p.append(n)
        while G.nodes[n]['prev'] != 1 and G.nodes[n]['prev'] is not None:
            p.append(G.nodes[n]['prev'])
            n = G.nodes[n]['prev']
        p.append(s)
        p.reverse()
        for n in p[:-1]:   
                string += f"{n}->"
        string += f"{node}\n"
        p = []
    return string

def create_dist_matrix(g):
    dmat=[]
    for node in g:
        dijkstra(g,node)
        dmat.append([0 for _ in range(len(g.nodes))])
        for dist in g.nodes.data("cost"):
            dmat[-1][dist[0]-1]=dist[1]
    return dmat

def sum_dist_min(g):
    mat=[sum(x) for x in create_dist_matrix(g)]
    m=min(mat)
    return (mat.index(m)+1,m) # centrum, najmniejsza sumaryczna odleglosc do wszystkich pozostalych wierzcholkow

def max_dist_min(g):
    mat=[max(x) for x in create_dist_matrix(g)]
    m=min(mat)
    return (mat.index(m)+1,m) # centrum minimax - najmniejsza odl od najdlaszego wierzchołka

def minimal_spanning_tree_Prim(g):
    g=g.copy()
    n=len(g.nodes)
    t = nx.Graph()
    node=1 # startowy wierzchołek
    t.add_node(node)
    ce=[]
    while len(t.nodes)!=n: # dopóki drzewo nie jest zbudowane
        try:
            ce.extend(g.edges(node,data=True)) # dodajemy krawędzie z node do drzewa
        except:
            raise Exception("Error")
        next_node=min(ce, key=lambda x: x[2]['weight']) # wybieramy krawędź lekką
        ce.remove(next_node) # usuwamy krawędź z ce
        t.add_edge(*next_node[:2],weight=next_node[2]['weight']) # i dodajemy ją do drzewa
        g.remove_node(node)
        node=next_node[1] # wybieramy kolejną krawędź
        ce=list(filter(lambda x: x[1]!=node, ce)) # aktualizujemy zbiór ce (usuwamy z niego node)
    return t

def minimal_spanning_tree_Kruskal(g):
    g=g.copy()
    n=len(g.nodes)
    t = nx.Graph()
    while len(t.edges)!=n-1: # waruenk końca
        edge=min(g.edges(data=True), key=lambda x: x[2]['weight']) # krawędź o najmniejszej wadze
        g.remove_edge(*edge[:2]) # usuwamy krawędź z grafu
        if edge[0] not in t or edge[1] not in t or components(t)[edge[0]] != components(t)[edge[1]]: # jeśli krawędź nie jest w drzewie lub jest w drzewie ale nie jest w tym samym składzie
            t.add_edge(*edge[:2],weight=edge[2]['weight']) # dodajemy do drzewa
    return t

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

if __name__ == '__main__':
    print(check_sequence([4,2,2,3,2,1,4,2,2,2,2]))
    a = create_graph_from_sequence([4,2,2,3,2,1,4,2,2,2,2])
    g = nx.Graph()
    g.add_nodes_from([i for i in range(1, 13)])
    g.add_weighted_edges_from([(1,2,3), (1,3,2), (1,5,9), (2,4,2), (2,5,4), (3,5,6), (3,6,9),
                            (4,7,3), (5,7,1), (5,8,2), (6,8,1), (6,9,2), (7,10,5), (8,10,5),
                            (8,11,6), (8,12,9), (9,11,2), (10,12,5), (11,12,3)])
    
    
    dijkstra(g,1)


    #print(create_dist_matrix(g))
    print(sum_dist_min(g))
    print(max_dist_min(g))
    print(minimal_spanning_tree_Prim(g).edges())
    # print(components(g))
    print(minimal_spanning_tree_Kruskal(g).edges())
    
    
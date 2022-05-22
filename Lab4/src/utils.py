from src.digraph import Digraph
import networkx as nx
import sys
import copy
import numpy as np
import random
import time

def generate_digraph(n, p):
    g = Digraph()
    g.add_vertices([_ for _ in range(1, n+1)])

    for vertex1 in g.get_vertices():
        for vertex2 in g.get_vertices():
            if vertex1 != vertex2 and random.uniform(0.0, 1.0) < p:
                g.add_edge(vertex1, vertex2)

    return g
    

def Kosaraj(g):
    d = {}
    f = {}
    
    for v in g.nodes():
        d[v] = -1 # czas odwierdzenia wierzchołka (-1 - nieodwiedzony)
        f[v] = -1 # czas przetworzenia wierzchołka (-1 - nieprzetworzony)

    t = 0
    for v in g.nodes():
        if d[v] == -1:
            t = kosaraj_visit(g, v, t, d, f)

    gt = g.reverse() # transpozycja grafu g
    nr = 0 # numer spójnej składowej
    comp = {}
    for v in gt.nodes():
        comp[v] = -1 # wszystkie wierzchołki nieodwiedzone

    for v in sorted(gt.nodes(), key=lambda x: f[x], reverse=True):
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_r(nr, v, gt, comp)

    return comp

def kosaraj_visit(g, v, t, d, f):
    t += 1
    d[v] = t
    for u in g.adj[v]:
        if d[u] == -1:
            t = kosaraj_visit(g, u, t, d, f)
    t += 1
    f[v] = t
    return t

def components_r(nr, v, gt, comp):
    for u in gt.adj[v]:
        if comp[u] == -1:
            comp[u] = nr
            components_r(nr, u, gt, comp)

def generate_strongly_connected_digraph(n, p):
    random.seed(time.time())
    g = generate_digraph(n, p)

    while not is_strongly_connected(Kosaraj(g.graph)):
        g = generate_digraph(n, p)
    
    nx.set_edge_attributes(g.graph, {e: {'weight': random.randint(-1, 9)} for e in g.graph.edges})
    
    return g

def is_strongly_connected(comp):
    if 2 in comp.values():
        return False
    return True

def init(G, s): 
    nx.set_node_attributes(G, sys.maxsize, 'cost') #ustawiam koszt dotarcia do węzła jako inf
    nx.set_node_attributes(G, None, 'prev') #ustawiam poprzednika na nieistenijącego
    G.nodes[s]['cost'] = 0 #ustawiam koszt dotarcia do wezła startowego jako 0 i jego poprzednika jako null

def relax(G, prev_node, current_node):
    if G.nodes[current_node]['cost'] > G.nodes[prev_node]['cost'] + G[prev_node][current_node]['weight']: #jezeli koszt dotarcia do wezla jest wiekszy niz koszt dotarcia do poprzednika + waga krawedzi miedzy nimi
        G.nodes[current_node]['cost'] = G.nodes[prev_node]['cost'] + G[prev_node][current_node]['weight'] # to ustawiam koszt dotarcia do konkretnego wezla jako suma kosztow
        G.nodes[current_node]['prev'] = prev_node #ustawiam poprzednika


def print_graph_paths(G,s): #wyswietla sciezki oraz koszty dotarcia do grafu G graf, s startowy wezeł
    for node in G:
        string = ""
        print(f"cost from node {s} -> {node} ==> {G.nodes[node]['cost']} Path:  {node}", end = "")
        while G.nodes[node]['prev'] != 1 and G.nodes[node]['prev'] is not None:
            string += f" -> {G.nodes[node]['prev']}"
            node = G.nodes[node]['prev']
        print(f"{string}")
        
def find_bellman_ford_path(G, s): #zwraca true jeżeli nie ma ujemnych cykli false jak jest
    init(G, s) 
    for i in range(len(G.nodes())-1):
        for edge in G.edges():
            relax(G, edge[0], edge[1]) #lecimy po każdej krawędzi i liczymy koszta dotarcia do każdego noda
    for edge in G.edges():
        if G.nodes[edge[1]]['cost'] > G.nodes[edge[0]]['cost'] + G[edge[0]][edge[1]]['weight']: #sprawdzam czy nie ma ujemnego cyklu
            return False
    print_graph_paths(G, s)
    h = {}
    for node in G:
        h[node] = G.nodes[node]['cost']
    return (True, h)


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
    list_of_costs = [] #na potrzeby zadania 4 robię zeby dijkstra zwracal liste odleglosci od danego noda do wszystkich innych
    for node in G:
        list_of_costs.append(G.nodes[node]['cost'])
    return list_of_costs

def add_s(G): #robi dodatkowy wierzchołek i prowadzi krawędzie do każdego istniejacego z wagą równą 0
    G_X = copy.deepcopy(G) #działam na kopi bo potem oryginał jest potrzebny
    G_X.add_node(len(G.nodes())+1) #+1 wierzcholek 
    num_of_nodes = len(G_X.nodes())
    for node in range(1,num_of_nodes): 
        G_X.add_edge(num_of_nodes, node, weight = 0) #dodaje krawędzie od nowego wierzchołka do każdnego innego noda
    return G_X #zwracam kopie

def johnson(G):
    G_X = add_s(G)
    (result, h) = find_bellman_ford_path(G_X, len(G_X.nodes()))
    if not result:
        raise ValueError("Graph contains negative cycle")

    G_X.remove_node(len(G_X.nodes())) #usuwam dodatkowy wierzchołek
    for u, v in G_X.edges():
        G_X[u][v]['weight'] = G_X[u][v]['weight'] + h[u] - h[v]
    
    D = []
    for u in G.nodes():
        D.append(dijkstra(G_X,u)) #dodajemy do macierzy odległosci policzone odleglosci od kazdego noda
        for v in G.nodes():
            D[u-1][v-1] = D[u-1][v-1] - h[u] + h[v]
    print(D)
    return D


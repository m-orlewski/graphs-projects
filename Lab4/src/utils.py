from src.digraph import Digraph
import networkx as nx
import sys

def Kosaraj(digraph):
    g = digraph.graph # nie potrzebujemy klasy Digraph, wystarczy nx.DiGraph()
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
        
def find_bellman_ford_path(G, s):
    init(G, s)
    for node in G.nodes:
        for edge in G.edges(node):
            relax(G, edge[0], edge[1])
    for edge in G.edges():
        if G.nodes[edge[1]]['cost'] > G.nodes[edge[0]]['cost'] + G[edge[0]][edge[1]]['weight']:
            return False
    print_graph_paths(G, s)
    return True



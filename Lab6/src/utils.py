from src.digraph import Digraph
import networkx as nx
import random
import numpy as np


def generate_digraph(n, p):
    g = Digraph()
    g.add_vertices([_ for _ in range(1, n+1)])

    for vertex1 in g.get_vertices():
        for vertex2 in g.get_vertices():
            if vertex1 != vertex2 and random.uniform(0.0, 1.0) < p:
                g.add_edge(vertex1, vertex2)

    return g

def page_rank_a(g,d=0.15,maxk=1e6):
    g_r = Digraph(from_graph=g).to_adj_list().representation #pobranie reprezentacji
    mx=max(g_r.keys()) #ilość węzłów grafu
    odw = {i:0 for i in range(1,mx+1)} #słownik ilosci odwiedzen
    k=0 #licznik iteracji
    node=random.randrange(1,mx+1) #wybeiramy losowy węzeł
    odw[node]+=1 #zwiekszamy ilość odwiedzeń wybranego węzła
    while k<maxk:
        k+=1 
        if random.random()<d: #sprawdzamy prawdopodobieństwo teleportacji
            node=random.randrange(1,mx+1) #teleportacja losujemy węzeł
            odw[node]+=1
        else:
            node=random.choice(g_r[node]) #brak teleporatcji wybieramy losowy wezeł z możliwych z wyjsciem
            odw[node]+=1

    w=[(x[0],x[1]/maxk) for x in odw.items()] #formatowanie danych
    return sorted(w, key=lambda x:x[1]) #sortowanie

def page_rank_b(g,d=0.15,maxk=1e6):
    am = np.asmatrix(Digraph(from_graph=g).to_adj_matrix().representation) #pobranie reprezentacji
    n=len(am) #ilość węzłów grafu
    w = [1/n for _ in range(1,n+1)] #wektor obsadzeń w t
    dj=[] 
    for i in range(len(am)):
        dj.append(np.count_nonzero(am[i,:]==1)) # dj stopnie wyjściowym wierzchołków j
    k=1 #licznik iteracji
    P=((1-d)*am/dj)+np.ones((n,n))*d/n #stworzenie macierzy stochastycznej P
    wn = w*P #wyznaczneie wektora obsadzeń w t+1
    s=np.sum(np.abs(wn)) # do warunku zakończenia
    while s>np.sum(np.abs(wn-w)): #warunek zakończenia pętli
        s=np.sum(np.abs(wn-w))
        k+=1
        w=wn
        wn = w*P #wyznaczneie wektora obsadzeń w t+1

    try: #formatowanie wyniku
        w=[(i,w[0,i-1]) for i in range(1,n+1)]
    except:
        w=[(i,w[i-1]) for i in range(1,n+1)]
    return sorted(w, key=lambda x:x[1]) #sortowanie
    
if __name__ == '__main__':
    n=10
    g = generate_digraph(n, 0.15).graph
    adj_list = Digraph(from_graph=g).to_adj_list()
    while min(adj_list.representation.values(), key=len)==[]:
        g = generate_digraph(n, 0.2).graph
        adj_list = Digraph(from_graph=g).to_adj_list()

    # print(np.ones([3,3])*2)
    print(Digraph(from_graph=g).to_adj_list().representation)
    # print(page_rank_a(g))
    wa=page_rank_a(g)
    w=page_rank_b(g)
    w2={i:w[0,i-1] for i in range(1,n+1)}
    # print(w2)
    wa=sorted(wa, key=wa.get)
    w2=sorted(w2, key=w2.get)
    print(wa)
    print(w2)



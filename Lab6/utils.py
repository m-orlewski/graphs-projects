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
    g_r = Digraph(from_graph=g).to_adj_list().representation
    mx=max(g_r.keys())
    odw = {i:0 for i in range(1,mx+1)}
    k=0
    node=random.randrange(1,mx+1)
    odw[node]+=1
    while k<maxk:
        k+=1
        if random.random()<d:
            node=random.randrange(1,mx+1)
            odw[node]+=1
        else:
            node=random.choice(g_r[node])
            odw[node]+=1

    return {x[0]:x[1]/maxk for x in odw.items()}

def page_rank_b(g,d=0.15,maxk=1e6):
    am = np.asmatrix(Digraph(from_graph=g).to_adj_matrix().representation)
    n=len(am)
    w = [1/n for _ in range(1,n+1)]
    k=0
    P=((1-d)*am/range(1,n+1))+d/n
    wn = w*P
    while np.max(np.abs(wn-w))>0.0001:
        k+=1
        w=(w+wn)/2
        wn = w*P

    print(k)
    return wn
    # node=random.randrange(1,mx+1)
    # odw[node]+=1
    # while k<maxk:
    #     k+=1
    #     if random.random()<d:
    #         node=random.randrange(1,mx+1)
    #         odw[node]+=1
    #     else:
    #         node=random.choice(g_r[node])
    #         odw[node]+=1

    # return {x[0]:x[1]/maxk for x in odw.items()}
    
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



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



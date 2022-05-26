import networkx as nx
import random, time

class FlowNetwork:
    def __init__(self, N):
        self.N = N
        self.graph = nx.DiGraph()

        # Wierzchołek startowy
        self.add_node('s', 0)

        self.next_node = 1

        # Wierzchołki w warstwach (od 1 do N)
        for layer in range(1, N+1):
            r = random.randint(2, N)
            for i in range(r):
                self.add_node(self.next_node, layer)
                self.next_node += 1

        # Wierzchołek końcowy
        self.add_node('t', N+1)

        # Krawędzie z wierzchołka 's'
        for node in self.get_nodes_from_layer(1):
            #print(f's -> {node}')
            self.add_edge('s', node, random.randint(1, 10))

        # Krawędzie z wierzchołków warstw (1, N-1)
        for layer in range(1, N):
            current_layer_nodes = self.get_nodes_from_layer(layer)
            next_layer_nodes = self.get_nodes_from_layer(layer+1)

            for node1 in current_layer_nodes:
                neighbors = random.sample(next_layer_nodes, random.randint(1, len(next_layer_nodes)))
                for node2 in neighbors:
                    # z każdego wierzchołka warstwy i wychodzi co najmniej 1 krawędź do warstwy i+1
                    #print(f'{node1} -> {node2}')
                    self.add_edge(node1, node2, random.randint(1, 10))

            for node2 in next_layer_nodes:
                # do każdego wierzchołka warstwy i+1 wchodzi co najmniej 1 krawędź z warstwy i
                if self.graph.in_degree(node2) == 0:
                    node1 = random.choice(current_layer_nodes)
                    #print(f'{node1} -> {node2}')
                    self.add_edge(node1, node2, random.randint(1, 10))

        # Krawędzie do wierzchołka 't'
        for node in self.get_nodes_from_layer(N):
            #print(f'{node} -> t')
            self.add_edge(node, 't', random.randint(1, 10))

        # Dodatkowe 2N krawędzi
        start_nodes = [_ for _ in range(1, self.next_node)]
        start_nodes.append('s')
        end_nodes = [_ for _ in range(1, self.next_node)]
        end_nodes.append('t')
        for i in range(2*N):
            node1 = random.choice(start_nodes)
            node2 = random.choice(end_nodes)

            while node1 == node2 or self.graph.has_edge(node1, node2) or self.graph.has_edge(node2, node1):
                node1 = random.choice(start_nodes)
                node2 = random.choice(end_nodes)

            self.add_edge(node1, node2, random.randint(1, 10))

        self.graph = self.create_test_graph()
        
        for u, v, data in self.graph.edges(data=True):
            self.graph.add_edge(v, u, capacity=data['capacity'], flow=0, reverse=True)

        for u, v in self.graph.edges():
            print(f'{u} -> {v}')


    def create_residual_graph(self):
        self.residual_graph = nx.DiGraph()
        for node in self.graph.nodes():
            self.residual_graph.add_node(node, layer=self.graph.nodes[node]['layer'])

        for node1, node2, data in self.graph.edges(data=True):
            flow = data['flow']
            capacity = data['capacity']

            self.residual_graph.add_edge(node2, node1, capacity=capacity-flow, flow=0)


    def add_node(self, node, layer):
        self.graph.add_node(node, layer=layer)

    def add_edge(self, node1, node2, capacity):
        self.graph.add_edge(node1, node2, capacity=capacity, flow=0)

    def get_nodes_from_layer(self, layer):
        return [node for node in self.graph.nodes() if self.graph.nodes[node]['layer'] == layer]

    def __str__(self):
        result = 'Node(layer) : neighbor(flow/capacity)\n'
        for node in self.graph.nodes():
            result += f'{node}({self.graph.nodes[node]["layer"]}) : '
            for neighbor in self.graph.neighbors(node):
                result += f'{neighbor}({self.graph.edges[node, neighbor]["flow"]}/{self.graph.edges[node, neighbor]["capacity"]}), '

            result = result[:-2] + '\n'

        return result
    
    def ford_fulkerson(self):
        flow = 0
        while True:
            path = self.bts('s', 't')
            if path is None:
                break

            u, v = path[0][0], path[0][1]
            cf = self.graph.edges[u, v]['capacity'] - self.graph.edges[u, v]['flow']
            for u, v in path:
                cf = min(cf, self.graph.edges[u, v]['capacity'] - self.graph.edges[u, v]['flow'])

            for u, v in path:
                self.graph.edges[u, v]['flow'] += cf
                self.graph.edges[v, u]['flow'] -= cf

            input()
            flow += cf

        return flow

    def bts(self, s, t):
        d, p = {}, {}
        for v in self.graph.nodes():
            d[v] = float('inf')
            p[v] = None

        d[s] = 0
        q = [s]

        while q:
            v = q.pop(0)
            for u in self.graph.neighbors(v):
                if d[u] == float('inf') and self.graph.edges[v, u]['flow'] < self.graph.edges[v, u]['capacity']:
                    print(f"If passed ({v}, {u}): {self.graph.edges[v, u]['flow']} < {self.graph.edges[v, u]['capacity']}")
                    d[u] = d[v] + 1
                    p[u] = v
                    q.append(u)

                    if u == t:
                        return self.get_path(p, s, t)
        return None

    def get_path(self, p, s, t):
        path = []
        while t != s:
            path.append((p[t], t))
            t = p[t]
        path.append((p[t], t))
        path = path[::-1]
        path = path[1::]
        return path 
            

    def create_test_graph(self):
        graph = nx.DiGraph()
        graph.add_node('s', layer = 0)

        graph.add_node('a', layer = 1)
        graph.add_node('b', layer = 1)
        graph.add_node('c', layer = 1)

        graph.add_node('d', layer = 2)
        graph.add_node('e', layer = 2)
        graph.add_node('f', layer = 2)

        graph.add_node('g', layer = 3)
        graph.add_node('h', layer = 3)
        graph.add_node('i', layer = 3)

        graph.add_node('t', layer = 4)
        #S -> 
        graph.add_edge('s', 'a', capacity = 10, flow = 0, reverse=False)
        graph.add_edge('s', 'b', capacity = 3, flow = 0, reverse=False)
        graph.add_edge('s', 'c', capacity = 6, flow = 0, reverse=False)
        #A -> 
        graph.add_edge('a', 'b', capacity = 8, flow = 0, reverse=False)
        graph.add_edge('a', 'd', capacity = 8, flow = 0, reverse=False)
        graph.add_edge('a', 'e', capacity = 6, flow = 0, reverse=False)
        #B ->
        graph.add_edge('b', 'e', capacity = 2, flow = 0, reverse=False)
        graph.add_edge('b', 'f', capacity = 10, flow = 0, reverse=False)
        #C -> 
        graph.add_edge('c', 'd', capacity = 10, flow = 0, reverse=False)
        graph.add_edge('c', 'f', capacity = 1, flow = 0, reverse=False)
        #D ->
        graph.add_edge('d', 'h', capacity = 5, flow = 0, reverse=False)
        #E ->
        graph.add_edge('e', 'i', capacity = 7, flow = 0, reverse=False)
        #F ->
        graph.add_edge('f', 'g', capacity = 10, flow = 0, reverse=False)
        #G -> 
        graph.add_edge('g', 't', capacity = 7, flow = 0, reverse=False)
        #H -> 
        graph.add_edge('h', 'g', capacity = 1, flow = 0, reverse=False)
        graph.add_edge('h', 't', capacity = 5, flow = 0, reverse=False)
        graph.add_edge('h', 'f', capacity = 8, flow = 0, reverse=False)
        #I ->
        graph.add_edge('i', 't', capacity = 7, flow = 0, reverse=False)

        return graph


if __name__ == '__main__':
    random.seed(time.time())
    f = FlowNetwork(3)
    print(f.ford_fulkerson())
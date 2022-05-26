import networkx as nx
import random, time

from pyparsing import conditionAsParseAction

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
            print(f's -> {node}')
            self.add_edge('s', node, random.randint(1, 10))

        # Krawędzie z wierzchołków warstw (1, N-1)
        for layer in range(1, N):
            current_layer_nodes = self.get_nodes_from_layer(layer)
            next_layer_nodes = self.get_nodes_from_layer(layer+1)

            for node1 in current_layer_nodes:
                neighbors = random.sample(next_layer_nodes, random.randint(1, len(next_layer_nodes)))
                for node2 in neighbors:
                    # z każdego wierzchołka warstwy i wychodzi co najmniej 1 krawędź do warstwy i+1
                    print(f'{node1} -> {node2}')
                    self.add_edge(node1, node2, random.randint(1, 10))

            for node2 in next_layer_nodes:
                # do każdego wierzchołka warstwy i+1 wchodzi co najmniej 1 krawędź z warstwy i
                if self.graph.in_degree(node2) == 0:
                    node1 = random.choice(current_layer_nodes)
                    print(f'{node1} -> {node2}')
                    self.add_edge(node1, node2, random.randint(1, 10))

        # Krawędzie do wierzchołka 't'
        for node in self.get_nodes_from_layer(N):
            print(f'{node} -> t')
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

        self.create_residual_graph() # Tworzymy sieć rezydualną

    def create_residual_graph(self):
        self.residual_graph = nx.DiGraph()
        for node in self.graph.nodes():
            self.residual_graph.add_node(node, layer=self.graph.nodes[node]['layer'])

        for node1, node2, data in self.graph.edges(data=True):
            flow = data['flow']
            capacity = data['capacity']

            self.residual_graph.add_edge(node1, node2, capacity=capacity-flow)
            self.residual_graph.add_edge(node2, node1, capacity=flow)


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

if __name__ == '__main__':
    random.seed(time.time())
    f = FlowNetwork(2)
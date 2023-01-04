'''Graph ADT'''
import math

class Graph:
    '''Graph ADT'''
    def __init__(self):
        self.max_vertecies = 10
        self.adjMatrix = []
        self.vertecies = []
        self.dfslyst  = []
        self.visited = []
        for i in range(self.max_vertecies):
            self.adjMatrix.append([0 for i in range(self.max_vertecies)])

        for i in range(self.max_vertecies):
            for x in range(self.max_vertecies):
                self.adjMatrix[i][x] = math.inf

    def get_index(self, src):
        '''get index of vertex'''
        for i in range(len(self.vertecies)):
            if src == self.vertecies[i]:
                return i

        return -1

    def add_vertex(self, label):
        '''add vertex'''
        if not isinstance(label,str):
            raise ValueError

        self.vertecies.append(label)
        return self

    def add_edge(self, src, dest, weight):
        '''add edge'''
        if not isinstance(src,str) and not isinstance(dest,str):
            raise ValueError
        if not isinstance(weight,int) and not isinstance(weight,float):
            raise ValueError

        from_index = self.get_index(src)
        to_index = self.get_index(dest)

        if from_index == -1 or to_index == -1:
            raise ValueError

        self.adjMatrix[from_index][to_index] = weight
        return self

    def get_weight(self, src, dest):
        '''get the weight of edge'''
        from_index = self.get_index(src)
        to_index = self.get_index(dest)
        return self.adjMatrix[from_index][to_index]

    def bfs(self, starting_vertex):
        '''breadth first search'''
        visited = [False] * len(self.vertecies)
        start = self.get_index(starting_vertex)
        queue = [start]
        visited[start] = True
        data = []

        while queue :
            vis = queue [0]
            data.append(self.vertecies[vis])
            queue .pop(0)

            for i in range(len(self.vertecies)):
                if (self.adjMatrix[vis][i] != math.inf and
                      (not visited[i])):
                    queue .append(i)
                    visited[i] = True
        return data

    def dfs(self, starting_vertex):
        '''depth first search'''
        lyst = []
        visited = [False for x in range(10)]
        return self.in_dfs(starting_vertex, visited, lyst)

    def in_dfs(self, starting_vertex, visited, lyst):
        '''dps helper'''
        start = self.get_index(starting_vertex)
        lyst.append(starting_vertex)
        visited[start] = True

        for i in range(len(self.adjMatrix[start])):
            if (self.adjMatrix[start][i] != math.inf) and (not visited[i]):
                self.in_dfs(self.vertecies[i], visited, lyst)

        return lyst

    def dsp(self, src, dest):
        '''dsp'''
        if src == dest:
            return(0,[src])
        adj_dict = {}
        shortest_distance = {}
        predecessor = {}
        path = []

        for i in range(len(self.adjMatrix)):
            for x in range(len(self.adjMatrix)):
                if self.adjMatrix[i][x] != math.inf:
                    path_tuple = (self.vertecies[i], self.vertecies[x])
                    adj_dict[path_tuple] = self.adjMatrix[i][x]

        path_lengths = {v: float('inf') for v in self.vertecies}
        path_lengths[src] = 0

        adj_nodes = {v: {} for v in self.vertecies}
        for (ult,val), w_uv in adj_dict.items():
            adj_nodes[ult][val] = w_uv

        unseen_nodes = adj_nodes

        for node in unseen_nodes:
            shortest_distance[node] = math.inf
        shortest_distance[src] = 0

        while unseen_nodes:
            minNode = None
            for node in unseen_nodes:
                if minNode is None:
                    minNode = node
                elif shortest_distance[node] < shortest_distance[minNode]:
                    minNode = node

            for child_node, weight in adj_nodes[minNode].items():
                if weight + shortest_distance[minNode] < shortest_distance[child_node]:
                    shortest_distance[child_node] = weight + shortest_distance[minNode]
                    predecessor[child_node] = minNode

            unseen_nodes.pop(minNode)

        current_node = dest
        while current_node:
            try:
                if predecessor[current_node]:
                    path.insert(0, current_node)
                    current_node = predecessor[current_node]

            except KeyError:
                break

        path.insert(0, src)
        if shortest_distance[dest] != math.inf and self.adjMatrix[self.get_index(src)][self.get_index(path[1])]:
            return (shortest_distance[dest], path)

        return (math.inf, [])

    def dsp_all(self, src):
        '''dsp all'''
        path = {}
        for item in self.vertecies:
            path[item] = self.dsp(src,item)[1]

        return path

    def __str__(self):
        '''str representation'''
        string = "digraph G {\n"
        for i in range(len(self.vertecies)):
            for x in range(len(self.adjMatrix[i])):
                if self.adjMatrix[i][x] != math.inf:
                    string += f"   {self.vertecies[i]} -> {self.vertecies[x]} [label=\"1.0\",weight=\"{self.adjMatrix[i][x]}\"];\n"
        string += "}\n"
        return string


def main():
    '''driver code'''
    g = Graph()
    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 10)
    g.add_edge('b', 'c', 13.0)
    g.add_edge('a', 'c', 9.5)
    g.add_edge('d', 'c', 6)
    g.add_edge('e', 'c', 3)
    g.add_edge('e', 'a', 1.0)
    g.add_edge('c', 'f', 2.0)
    g.add_edge('b', 'd', 3.0)
    g.add_edge('d', 'f', 2.3)

    print(g)

    print("DFS Search of A: ")
    print(g.dfs('a'))

    print("BFS Search of B: ")
    print(g.bfs('b'))

    #dsp and dsp_all
    print("DSP for A -- F: ")
    print(g.dsp('a','f'))

    print("DSP all paths for A:")
    print(g.dsp_all('a'))

main()

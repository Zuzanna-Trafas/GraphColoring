import random
import copy


class Graph:
    def __init__(self, size):
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.colors = [0 for _ in range(size)]

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.matrix])

    def color(self, vertex, color):
        self.matrix[vertex][vertex] = color
        self.colors[vertex] = color

    def add_edge(self, vertex1, vertex2):
        self.matrix[vertex1-1][vertex2-1] = 1
        self.matrix[vertex2-1][vertex1-1] = 1

    def greedy_coloring(self, starting_vertex):
        for vertex in range(starting_vertex, starting_vertex + len(self.matrix)):
            colors = []
            color = 0
            for other_vertex in range(len(self.matrix)):
                if self.matrix[vertex % len(self.matrix)][other_vertex] == 1 and self.matrix[other_vertex][other_vertex] not in colors:
                    colors.append(self.matrix[other_vertex][other_vertex])
            for i in range(1, len(colors)+2):
                if i not in colors:
                    color = i
                    break
            self.color(vertex % len(self.matrix), color)
        maximum = 0
        for c in range(len(self.matrix)):
            if self.matrix[c][c] > maximum:
                maximum = self.matrix[c][c]
        return maximum

    def optimized_greedy_coloring(self):
        neighbor_list = []
        vertex_list = list(range(len(self.matrix)))
        for vertex in range(len(self.matrix)):
            neighbors = sum(self.matrix[vertex]) - self.matrix[vertex][vertex]
            neighbor_list.append(neighbors)
        sorted_vertex_list = [x for _, x in sorted(zip(neighbor_list, vertex_list), reverse=True)]
        for vertex in sorted_vertex_list:
            colors = []
            color = 0
            for other_vertex in range(len(self.matrix[vertex])):
                if self.matrix[vertex][other_vertex] == 1 and self.matrix[other_vertex][other_vertex] not in colors:
                    colors.append(self.matrix[other_vertex][other_vertex])
            for i in range(1, len(colors) + 2):
                if i not in colors:
                    color = i
                    break
            self.color(vertex, color)
        maximum = 0
        for c in range(len(self.matrix)):
            if self.matrix[c][c] > maximum:
                maximum = self.matrix[c][c]
        return maximum


def graph_generator(density, vertex_number, file_name):
    edges = []
    edge_number = vertex_number
    f = open(file_name, "w+")
    f.write(str(vertex_number) + "\n")
    for i in range(1, vertex_number):
        edges.append((i, i+1))
        f.write(str(i) + " " + str(i+1) + "\n")
    f.write("1 " + str(vertex_number) + "\n")
    edges.append((1, vertex_number))
    graph_density = (2 * edge_number) / (vertex_number * (vertex_number - 1))
    while graph_density <= density:
        a = random.randint(1, vertex_number)
        b = random.randint(1, vertex_number)
        while a == b or (a, b) in edges or (b, a) in edges:
            b = random.randint(1, vertex_number)
        edges.append((a, b))
        f.write(str(a) + " " + str(b) + "\n")
        edge_number += 1
        graph_density = (2 * edge_number) / (vertex_number * (vertex_number - 1))
    f.close()


def generate_population(graph_number, file):
    graphs = []
    f = open(file, "r")  # opening the file
    lines = f.readlines()  # storing content in lines variable
    vertex_number = int(lines[0])
    for _ in range(graph_number):
        g = Graph(vertex_number)
        for i in lines[1:]:
            vertices = i.split()
            g.add_edge(int(vertices[0]), int(vertices[1]))
        graphs.append(g)

    for i in range(len(graphs)):
        graphs[i].greedy_coloring(i)

    return graphs
    f.close()


"""
# CREATING GRAPH FROM FILE
#graph_generator(0.7, 10, "a.txt")
f = open("graph70.txt", "r")   # opening the file
lines = f.readlines()   # storing content in lines variable
vertex_number = int(lines[0])  # first line is vertex number
graph = Graph(vertex_number)
for i in lines[1:]:
    vertices = i.split()
    graph.add_edge(int(vertices[0]), int(vertices[1]))
graph2 = copy.deepcopy(graph)
print(graph.greedy_coloring(0))
#print(graph)
#print(graph2.greedy_coloring(2))
#print(graph2)
f.close()
"""
graph_generator(0.7, 10, "a.txt")
generate_population(5, "a.txt")

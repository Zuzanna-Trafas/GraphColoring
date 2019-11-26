import random
import copy


class Graph:
    def __init__(self, size):
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.colors = [0 for _ in range(size)]

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.matrix])

    def __eq__(self, other):
        return self.matrix == other.matrix

    def __hash__(self):
        return id(self)

    def color(self, vertex, color):
        self.matrix[vertex][vertex] = color
        self.colors[vertex] = color

    def find_errors(self):
        error_number = 0
        for vertex in range(len(self.matrix)):
            for other_vertex in range(vertex+1, len(self.matrix)):
                if self.matrix[vertex][other_vertex] == 1 and self.colors[vertex] == self.colors[other_vertex]:
                    error_number += 1
        return error_number

    def mutation(self):
        for vertex in range(len(self.matrix)):
            adjacent_colors = []
            for v in range(len(self.matrix)):
                if self.matrix[vertex][v] == 1:
                    adjacent_colors.append(self.colors[v])
            for i in range(1, self.colors[vertex]):
                if i not in adjacent_colors:
                    self.color(vertex, i)
            for other_vertex in range(vertex+1, len(self.matrix)):
                if self.matrix[vertex][other_vertex] == 1 and self.colors[vertex] == self.colors[other_vertex]:
                    for i in range(1, max(adjacent_colors)+2):
                        if i not in adjacent_colors:
                            self.color(vertex, i)
                            break

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
        return max(self.colors)

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


def crossover(parent1, parent2):
    a = random.randint(1, len(parent1.matrix))
    child = copy.deepcopy(parent1)
    child.colors[a:] = parent2.colors[a:]
    return child


def parent_selection1(graphs):
    parents = []
    for _ in range(2):
        a = random.randint(1, len(graphs)-1)
        b = random.randint(1, len(graphs)-1)
        while a == b:
            b = random.randint(1, len(graphs)-1)
        max_a = max(graphs[a].colors)
        max_b = max(graphs[b].colors)
        if max_a > max_b:
            parent = graphs[b]
        else:
            parent = graphs[a]
        parents.append(parent)
    return parents


def parent_selection2(graphs):
    parents = []
    max_colors = {}
    for i in range(len(graphs)):
        max_colors[graphs[i]] = max(graphs[i].colors)
    v = list(max_colors.values())
    k = list(max_colors.keys())
    parents.append(k[v.index(min(v))])
    del max_colors[k[v.index(min(v))]]
    v = list(max_colors.values())
    k = list(max_colors.keys())
    parents.append(k[v.index(min(v))])
    return parents


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

    f.close()
    return graphs


def genetic(graphs):
    a = random.randint(1, 2)
    if a == 1:
        parents = parent_selection1(graphs)
    else:
        parents = parent_selection2(graphs)
    child = crossover(parents[0], parents[1])
    child.mutation()
    if child != graphs[-1]:
        graphs.append(child)
        maximum = 0
        max_index = 0
        for i in range(len(graphs)):
            if max(graphs[i].colors) > maximum:
                maximum = max(graphs[i].colors)
                max_index = i
        graphs.pop(max_index)
    return graphs


# graph_generator(0.7, 80, "a.txt")
graphs = generate_population(50, "queen6")

print("Minimalna liczba kolorów:")

print("zachlanny: " + str(max(graphs[0].colors)))

f = open("queen6", "r")   # opening the file
lines = f.readlines()   # storing content in lines variable
vertex_number = int(lines[0])  # first line is vertex number
graph = Graph(vertex_number)
for i in lines[1:]:
    vertices = i.split()
    graph.add_edge(int(vertices[0]), int(vertices[1]))

print("zoptymalizowany zachlanny: " + str(graph.optimized_greedy_coloring()))

for i in range(1000):
    graphs = genetic(graphs)
max_colors = {}
for i in range(len(graphs)):
    max_colors[graphs[i]] = max(graphs[i].colors)
v = list(max_colors.values())

print("genetyczny: " + str(min(v)))

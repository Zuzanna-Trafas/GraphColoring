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

    def mutation1(self):
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

    def mutation2(self):
        for vertex in range(len(self.matrix)):
            for other_vertex in range(vertex+1, len(self.matrix)):
                if self.matrix[vertex][other_vertex] == 1 and self.colors[vertex] == self.colors[other_vertex]:
                    self.color(vertex, max(self.colors)+1)

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


class Population:
    def __init__(self, graph_number, file):
        self.graphs = []
        self.graph_number = graph_number
        self.color_number = [0 for _ in range(self.graph_number)]
        f = open(file, "r")  # opening the file
        lines = f.readlines()  # storing content in lines variable
        vertex_number = int(lines[0])
        for _ in range(graph_number):
            g = Graph(vertex_number)
            for i in lines[1:]:
                vertices = i.split()
                g.add_edge(int(vertices[0]), int(vertices[1]))
            self.graphs.append(g)
        for i in range(len(self.graphs)):
            c = self.graphs[i].greedy_coloring(i)
            self.color_number[i] = c
        f.close()

    def parent_selection1(self):
        parents = []
        for _ in range(2):
            a = random.randint(1, self.graph_number - 1)
            b = random.randint(1, self.graph_number - 1)
            while a == b:
                b = random.randint(1, self.graph_number - 1)
            if self.color_number[a] > self.color_number[b]:
                parent = self.graphs[b]
            else:
                parent = self.graphs[a]
            parents.append(parent)
        return parents

    def parent_selection2(self):
        i = 0
        j = 0
        parent1, parent2 = self.color_number[0], self.color_number[0]
        for n in range(1, self.graph_number):
            color = self.color_number[n]
            if color <= parent1:
                parent1, parent2 = color, parent1
                i, j = n, i
            elif color < parent2:
                parent2 = color
                j = n
        return self.graphs[i], self.graphs[j]

    def crossover(self, parents):
        parent1 = parents[0]
        parent2 = parents[1]
        a = random.randint(1, len(parent1.matrix))
        child = copy.deepcopy(parent1)
        child.colors[a:] = parent2.colors[a:]
        return child

    def genetic(self):
        added_number = 0
        colors = copy.deepcopy(self.color_number)
        while added_number < self.graph_number//2:
            seed = random.randint(0, 1)
            if seed == 0:
                parents = self.parent_selection1()
                child = self.crossover(parents)
                child.mutation2()

            else:
                parents = self.parent_selection2()
                child = self.crossover(parents)
                child.mutation1()

            already_exist = False
            for i in range(self.graph_number):
                if child == self.graphs[i]:
                    already_exist = True

            if already_exist is False:
                idx = colors.index(max(colors))
                colors[idx] = 0
                self.graphs[idx] = child
                self.color_number[idx] = len(set(child.colors))
                added_number += 1


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


graphs = Population(50, "queen6")
print(graphs.color_number[0])
for i in range(1000):
    graphs.genetic()
    print(graphs.color_number)
    print(min(graphs.color_number))
print(min(graphs.color_number))


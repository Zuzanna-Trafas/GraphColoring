import random
import copy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


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

    def random_coloring(self):
        for i in range(len(self.matrix)):
            self.color(i, random.randint(1, len(self.matrix)+1))
        self.mutation1()
        return len(set(self.colors))

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

    def visualization(self):
        a = nx.from_numpy_matrix(np.matrix(self.matrix))
        pos = nx.circular_layout(a)
        nx.draw(a, pos=pos, with_labels=False, node_color=self.colors, cmap=plt.cm.gist_rainbow)
        plt.show()


class Population:
    def __init__(self, graph_number, file):
        self.graphs = {}
        self.graph_number = graph_number
        self.similarity = {}
        self.graphs_rate = {}
        f = open(file, "r")  # opening the file
        lines = f.readlines()  # storing content in lines variable
        vertex_number = int(lines[0])
        for _ in range(graph_number):
            g = Graph(vertex_number)
            for i in lines[1:]:
                vertices = i.split()
                g.add_edge(int(vertices[0]), int(vertices[1]))
            self.graphs[g] = 0
        for graph in self.graphs:
            c = graph.random_coloring()  # random coloring, we might try adding one greedy
            self.graphs[graph] = c
        c = graph.greedy_coloring(0)
        self.graphs[graph] = c
        f.close()

    """
    similarity_rate
    for each graph we assign the biggest similarity to another graph in population
    similarity is the number of the same vertices (same colors) in two graphs
    """
    def similarity_rate(self):
        keys = [g for g in self.graphs]
        vertex_number = len(keys[0].matrix)
        for g in range(len(keys)):
            biggest_similarity = 0
            for g2 in range(g + 1, len(keys)):
                sim = 0
                for c in range(vertex_number):
                    if keys[g] == keys[g2]:
                        break
                    if keys[g].colors[c] == keys[g2].colors[c]:
                        sim += 1
                if biggest_similarity < sim:
                    biggest_similarity = sim
            self.similarity[keys[g]] = biggest_similarity
        values = [value for value in self.similarity.values()]
        return max(values)

    """
    excluder
    updates graph_rate, for each graph we assign the normalized scores for similarity and color number
    we want to minimize both
    possible to change weights of variables (similarity and number of colors)
    """
    def excluder(self):
        colors = [value for value in self.graphs.values()]
        max_similarity = self.similarity_rate()
        max_colors = max(colors)
        for i in self.graphs:
            self.graphs_rate[i] = (self.similarity[i] / max_similarity)*5 + (self.graphs[i] / max_colors)  # weights
        return max(self.graphs_rate, key=self.graphs_rate.get)

    def parent_selection1(self):
        parents = []
        for _ in range(2):
            a = random.choice(list(self.graphs))
            b = random.choice(list(self.graphs))
            while a == b:
                b = random.choice(list(self.graphs))
            if self.graphs[a] > self.graphs[b]:
                parents.append(b)
            else:
                parents.append(a)
        return parents

    def parent_selection2(self):
        p1, p2 = 0, 0
        parent1, parent2 = 1000, 1000
        for n in self.graphs:
            color = self.graphs[n]
            if color <= parent1:
                parent1, parent2 = color, parent1
                p1, p2 = n, p1
            elif color < parent2:
                parent2 = color
                p2 = n
        return [p1, p2]

    def crossover(self, parents):
        parent1 = parents[0]
        parent2 = parents[1]
        a = random.randint(1, len(parent1.matrix))
        child = copy.deepcopy(parent1)
        child.colors[a:] = parent2.colors[a:]
        return child

    """
    genetic
    we choose the graph with the biggest graph_rate, to replace it with a child
    as we count the graph_rates at the beginning, if for chosen graph we change it to 0, it will not be selected
    """
    def genetic(self):
        new_generation = {}
        self.excluder()
        x = min(self.graphs, key=self.graphs.get)
        new_generation[x] = len(set(x.colors))
        added_number = 0
        while added_number < self.graph_number//1.1:  # what part of population we want to update in this generation
            seed = random.randint(0, 50)
            """
            we can choose different combinations of parent selections and mutations
            or change the probability of choosing each combination
            """
            if seed < 10:
                parents = self.parent_selection2()
                child = self.crossover(parents)
                #if 0 <= seed < 4:
                child.mutation1()

            elif 10 <= seed < 40 :
                parents = self.parent_selection1()
                child = self.crossover(parents)
                #if 25<=seed<40:
                child.mutation2()
            elif 40<=seed<50:
                child = copy.deepcopy(random.choice(list(self.graphs)))
                seed = random.randint(0, len(child.matrix)-1)
                child.greedy_coloring(seed)
            else:
                parent1 = copy.deepcopy(random.choice(list(self.graphs)))
                parent1.random_coloring()
                parents = self.parent_selection1()
                parents[0] = parent1
                child = self.crossover(parents)

            already_exist = False
            for i in self.graphs:
                if i.colors == child.colors:
                    already_exist = True

            if already_exist is False:
                new_generation[child] = len(set(child.colors))
                added_number += 1

        while added_number < self.graph_number:
            g = min(self.graphs_rate, key=self.graphs_rate.get)
            new_generation[g] = len(set(g.colors))
            added_number += 1
        self.graphs = new_generation


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



# color number for greedy approach
file_name = "miles250.txt"
f = open(file_name, "r")
lines = f.readlines()
vertex_number = int(lines[0])
g = Graph(vertex_number)
g2 = Graph(vertex_number)
for i in lines[1:]:
     vertices = i.split()
     g.add_edge(int(vertices[0]), int(vertices[1]))
     g2.add_edge(int(vertices[0]), int(vertices[1]))
print("greedy algorithm: " + str(g.greedy_coloring(0)))
print("optimized greedy algorithm: " + str(g2.optimized_greedy_coloring()))
graphs = Population(50, file_name)  # choosing the size of population
generation_number = 200
for i in range(generation_number):  # number of generations
    graphs.genetic()
    # with this we can see the differences in colors between generations
    for j in graphs.graphs:
        print(j.colors)
    print(min(graphs.graphs.values()))
    if i % (generation_number//10) == 0:
        print("Progress: " + str(int(i/generation_number*100)) + "%")
print("genetic algorithm: " + str(min(graphs.graphs.values())))
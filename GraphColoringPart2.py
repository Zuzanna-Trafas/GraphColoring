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

    def color(self, vertex, color):
        self.colors[vertex] = color

    def add_edge(self, vertex1, vertex2):
        self.matrix[vertex1-1][vertex2-1] = 1
        self.matrix[vertex2-1][vertex1-1] = 1

    def greedy_coloring(self, starting_vertex):
        self.colors = [0 for _ in range(len(self.matrix))]
        for vertex in range(starting_vertex, starting_vertex + len(self.matrix)):
            colors = []
            color = 0
            for other_vertex in range(len(self.matrix)):
                if self.matrix[vertex % len(self.matrix)][other_vertex] == 1 and self.colors[other_vertex] not in colors:
                    colors.append(self.colors[other_vertex])
            for i in range(1, len(colors)+2):
                if i not in colors:
                    color = i
                    break
            self.color(vertex % len(self.matrix), color)
        return self.colors

    def optimized_greedy_coloring(self):
        neighbor_list = []
        vertex_list = list(range(len(self.matrix)))
        for vertex in range(len(self.matrix)):
            neighbors = sum(self.matrix[vertex])
            neighbor_list.append(neighbors)
        sorted_vertex_list = [x for _, x in sorted(zip(neighbor_list, vertex_list), reverse=True)]
        for vertex in sorted_vertex_list:
            colors = []
            color = 0
            for other_vertex in range(len(self.matrix[vertex])):
                if self.matrix[vertex][other_vertex] == 1 and self.colors[other_vertex] not in colors:
                    colors.append(self.colors[other_vertex])
            for i in range(1, len(colors) + 2):
                if i not in colors:
                    color = i
                    break
            self.color(vertex, color)
        return max(self.colors)

    def visualization(self, number):
        a = nx.from_numpy_matrix(np.matrix(self.matrix))
        pos = nx.circular_layout(a)
        colors = []
        for i in self.colors:
            if i == 1:
                colors.append("blue")
            if i == 2:
                colors.append("green")
            if i == 3:
                colors.append("red")
            if i == 4:
                colors.append("yellow")
            if i == 5:
                colors.append("orange")
            if i == 6:
                colors.append("pink")

        nx.draw(a, pos=pos, node_color=colors, with_labels=True)
        name = "Figure" + str(number)
        plt.savefig(name)

    def mutation(self):
        for vertex in range(len(self.matrix)):
            adjacent_colors = [0]
            for other_vertex in range(len(self.matrix)):
                if self.matrix[vertex][other_vertex] == 1:
                    adjacent_colors.append(self.colors[other_vertex])
            for i in range(1, max(adjacent_colors) + 2):
                if i not in adjacent_colors:
                    self.color(vertex, i)
                    break

        return self.colors

    def random_coloring(self):
        for i in range(len(self.matrix)):
            self.color(i, random.randint(1, len(self.matrix)))
        self.mutation()
        return self.colors

    def find_errors(self):
        error_number = 0
        for vertex in range(len(self.matrix)):
            for other_vertex in range(vertex+1, len(self.matrix)):
                if self.matrix[vertex][other_vertex] == 1 and self.colors[vertex] == self.colors[other_vertex]:
                    error_number += 1
        return error_number


class Population:

    def __init__(self, graph_number, file):
        self.graph_number = graph_number
        self.colors = []
        self.rate = [0 for _ in range(self.graph_number)]
        self.similarity = [0 for _ in range(self.graph_number)]
        f = open(file, "r")  # opening the file
        lines = f.readlines()  # storing content in lines variable
        vertex_number = int(lines[0])
        self.graph = Graph(vertex_number)
        for i in lines[1:]:
            vertices = i.split()
            self.graph.add_edge(int(vertices[0]), int(vertices[1]))
        for _ in range(graph_number):
            self.graph.random_coloring()
            self.colors.append(copy.deepcopy(self.graph.colors))
        # one greedy graph
        #self.graph.greedy_coloring(0)
        #self.colors.append(copy.deepcopy(self.graph.colors))
        f.close()

    def similarity_rate(self):  # counting biggest similarity to any other graph in population
        for g in range(len(self.colors)):
            biggest_similarity = 0
            for g2 in range(len(self.colors)):
                if g == g2:
                    continue
                similarity = 0
                for c in range(len(self.colors[0])):
                    if self.colors[g][c] == self.colors[g2][c]:
                        similarity += 1
                if biggest_similarity < similarity:
                    biggest_similarity = similarity
            self.similarity[g] = biggest_similarity
        return max(self.similarity)

    def exclude(self):  # counting rates for graphs where  big rate == bad graph
        max_similarity = self.similarity_rate()
        max_color_number = max([len(set(i)) for i in self.colors])
        for g in range(self.graph_number):
            self.rate[g] = (self.similarity[g] / max_similarity) * 5 + \
                           (len(set(self.colors[g])) / max_color_number)

    def parent_selection1(self):  # more random one
        parents = []
        for _ in range(2):
            a = random.randint(0, self.graph_number-1)
            b = random.randint(0, self.graph_number-1)
            while a == b:
                b = random.randint(0, self.graph_number-1)
            if len(set(self.colors[a])) > len(set(self.colors[b])):
                parents.append(self.colors[b])
            else:
                parents.append(self.colors[a])
        return parents

    def parent_selection2(self):  # more optimal one
        parent1, parent2 = self.colors[0], self.colors[0]
        for n in self.colors:
            if len(set(n)) <= len(set(parent1)):
                parent1, parent2 = n, parent1
            elif len(set(n)) < len(set(parent2)):
                parent2 = n
        return [parent1, parent2]

    def genetic(self, part_of_population, mutation=False):
        new_generation = []
        self.exclude()
        added_number = 0
        while added_number < self.graph_number * part_of_population:  # what part of population we want to update in this generation
            seed = random.randint(0, 100)
            if seed <= 20:  # generating greedy child
                g = random.randint(0, len(self.colors[0]))
                child = self.graph.greedy_coloring(g)
            else:
                if seed <= 70:  # generating a bit random-crossover child
                    parents = self.parent_selection2()
                else:  # generating optimal child from population
                    parents = self.parent_selection1()
                    if seed >= 90:
                        parents[0] = self.graph.random_coloring()
                child = crossover(parents)
                if mutation:
                    self.graph.colors = child
                    child = self.graph.mutation()
            already_exist = False
            for color in self.colors:
                if color == child:
                    already_exist = True

            if already_exist is False:
                new_generation.append(child)
                added_number += 1
        minimum_color = 500
        best_coloring = []
        for j in self.colors:
            x = len(set(j))
            if x < minimum_color:
                minimum_color = x
                best_coloring = j
        new_generation.append(best_coloring)
        added_number += 1
        while added_number < self.graph_number:
            selected = self.colors[self.rate.index(min(self.rate))]
            new_generation.append(selected)
            added_number += 1
        self.colors = new_generation

    def mutate_all(self):
        for k in range(self.graph_number):
            self.graph.colors = self.colors[k]
            self.colors[k] = self.graph.mutation()

    def find_minimum(self, generation_number, part_of_population, how_often_mutate):
        for iter in range(generation_number):  # number of generations
            if iter % how_often_mutate == 0:
                self.genetic(part_of_population, mutation=True)
            else:
                self.genetic(part_of_population)
            if iter % (generation_number // 100) == 0:
                print("Progress: " + str(int(iter / generation_number * 100)) + "%")
                #self.mutate_all()
                minimum_color = 500
                for j in self.colors:
                    x = len(set(j))
                    if x < minimum_color:
                        minimum_color = x
                print(minimum_color)
        self.mutate_all()
        minimum_color = 500
        for j in self.colors:
            x = len(set(j))
            if x < minimum_color:
                minimum_color = x
        return minimum_color


def crossover(parents):
    a = random.randint(1, len(parents[0])-1)
    child = parents[0][:a] + parents[1][a:]
    return child


"""
find_minimum:
    generation_number: number of generations
    part_of_population: what part of population to replace in each generation [0-1]
    how_often_mutate: how often to mutate [2-infinity], where 2 means every two generations etc
    
"""


# color number for greedy approaches
file_name = "g6507"
f = open(file_name, "r")
lines = f.readlines()
vertex_number = int(lines[0])
g = Graph(vertex_number)
g2 = Graph(vertex_number)
for i in lines[1:]:
    vertices = i.split()
    g.add_edge(int(vertices[0]), int(vertices[1]))
    g2.add_edge(int(vertices[0]), int(vertices[1]))

print("greedy algorithm: " + str(max(g.greedy_coloring(0))))
print("optimized greedy algorithm: " + str(g2.optimized_greedy_coloring()))


# 3 times genetic algorithm
for _ in range(3):
    graphs = Population(30, file_name)  # choosing the size of population
    minimum = graphs.find_minimum(100, 0.8, 1)  # choosing parameters
    print("genetic algorithm: " + str(minimum))

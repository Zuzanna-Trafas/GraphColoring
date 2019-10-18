class Graph:
    def __init__(self, size):
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.matrix])

    def color(self, vertex, color):
        self.matrix[vertex][vertex] = color

    def add_edge(self, vertex1, vertex2):
        self.matrix[vertex1-1][vertex2-1] = 1
        self.matrix[vertex2-1][vertex1-1] = 1

def greedy_coloring(graph):
    for vertex in range(len(graph.matrix)):
        colors = []
        for other_vertex in range(len(graph.matrix[vertex])):
            if graph.matrix[vertex][other_vertex] == 1 and not graph.matrix[other_vertex][other_vertex]in colors:
                colors.append(graph.matrix[other_vertex][other_vertex])
        for i in range(1, len(colors)+2):
            if not i in colors:
                color = i
                break
        graph.color(vertex, color)
    return graph



# CREATING GRAPH FROM FILE
f = open("graf.txt", "r")   # opening the file
lines = f.readlines()   # storing content in lines variable
vertex_number = int(lines[0])  # first line is vertex number
graph = Graph(vertex_number)
for i in lines[1:]:
    vertices = i.split()
    graph.add_edge(int(vertices[0]), int(vertices[1]))
graph = greedy_coloring((graph))
print(graph)
f.close()

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

    def greedy_coloring(self):
        for vertex in range(len(self.matrix)):
            colors = []
            color = 0
            for other_vertex in range(len(self.matrix[vertex])):
                if self.matrix[vertex][other_vertex] == 1 and self.matrix[other_vertex][other_vertex] not in colors:
                    colors.append(self.matrix[other_vertex][other_vertex])
            for i in range(1, len(colors)+2):
                if i not in colors:
                    color = i
                    break
            self.color(vertex, color)



# CREATING GRAPH FROM FILE
f = open("graf.txt", "r")   # opening the file
lines = f.readlines()   # storing content in lines variable
vertex_number = int(lines[0])  # first line is vertex number
graph = Graph(vertex_number)
for i in lines[1:]:
    vertices = i.split()
    graph.add_edge(int(vertices[0]), int(vertices[1]))
graph.greedy_coloring()
print(graph)
f.close()

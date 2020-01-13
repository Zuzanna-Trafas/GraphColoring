import random

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

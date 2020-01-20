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


graph_generator(0.3, 350, "g3403")
print("XD1")
graph_generator(0.3, 650, "g6503")
print("XD2")
graph_generator(0.5, 200, "g2005")
print("XD3")
graph_generator(0.5, 350, "g3505")
print("XD4")
graph_generator(0.5, 500, "g5005")
print("XD5")
graph_generator(0.5, 650, "g6505")
print("XD6")
graph_generator(0.5, 800, "g8005")
print("XD7")
graph_generator(0.7, 350, "g3507")
print("XD8")
graph_generator(0.7, 650, "g6507")
print("XD9")
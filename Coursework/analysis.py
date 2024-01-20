from random import randint, random
import time
from adjacency_list_graph import AdjacencyListGraph
from adjacency_matrix_graph import AdjacencyMatrixGraph
from dijkstra import dijkstra
import matplotlib.pyplot as plt


def generate_random_graph(card_V, edge_probability, by_adjacency_lists=True, directed=True, weighted=False, min_weight=0, max_weight=20):
    constructor = AdjacencyListGraph if by_adjacency_lists else AdjacencyMatrixGraph
    G = constructor(card_V, directed, weighted)

    for u in range(card_V):
        if directed:
            min_v = 0
        else:
            min_v = u + 1

        for v in range(min_v, card_V):
            if random() <= edge_probability:  # add edge (u, v)
                if weighted:
                    weight = randint(min_weight, max_weight)  # random weight within range
                else:
                    weight = None
                G.insert_edge(u, v, weight)  # guaranteed that edge (u, v) is not already present

    return G

def dijkstra_on_random_graph(graph):
    source_vertex = randint(0, graph.get_card_V() - 1)

    # Measure the time taken by Dijkstra's algorithm
    start_time = time.time()
    dijkstra(graph, source_vertex)
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

# Generate a random graph
graph = generate_random_graph(10, 0.2)

# Apply Dijkstra's algorithm on the random graph
dijkstra_on_random_graph(graph)

# Number of iterations for the analysis
num_iterations = 100

# Collect elapsed times
elapsed_times = [dijkstra_on_random_graph(graph) for _ in range(num_iterations)]

# Plot histogram
plt.hist(elapsed_times, bins=20, color='blue', edgecolor='black')
plt.title('Dijkstra\'s Algorithm Execution Time Histogram')
plt.xlabel('Execution Time (seconds)')
plt.ylabel('Frequency')
plt.show()
import time
import matplotlib.pyplot as plt
from random import randint, random
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

def generate_random_graph(card_V, edge_probability, by_adjacency_lists=True,
                          directed=True, weighted=False, min_weight=0, max_weight=20):
    """Generate and return a random graph.

    Arguments:
        card_V -- number of vertices
        edge_probability -- probability that a given edge is present
        by_adjacency_lists -- True if the graph is represented by adjacency lists,
        False if by an adjacency matrix
        directed -- True if the graph is directed, False if undirected
        weighted -- True if the graph is weighted, False if unweighted
        min_weight -- if weighted, the minimum weight of an edge
        max_weight -- if weighted, the maximum weight of an edge

    Returns:
        A graph
        """
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

# Analysis function
def dijkstra_analysis(graph_sizes):
    execution_times = []

    for size in graph_sizes:
        graph = generate_random_graph(size, 0.12)
        execution_time = dijkstra_on_random_graph(graph)
        execution_times.append(execution_time)
        print(f"Graph of size {size} - Time taken: {execution_time} seconds")

    # Plotting the histogram
    plt.hist(execution_times, bins=10, color='blue', edgecolor='black')
    plt.title('Dijkstra Algorithm Execution Time on Random Graphs')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.show()

# Testing
if __name__ == "__main__":
    graph_sizes_to_test = [10, 20, 50, 100]
    dijkstra_analysis(graph_sizes_to_test)



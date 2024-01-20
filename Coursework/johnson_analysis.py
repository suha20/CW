import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_random_graph(card_V, edge_probability, by_adjacency_lists=True,directed=True, weighted=False, min_weight=0, max_weight=20):
    def generate_random_graph(card_V, edge_probability, by_adjacency_lists=True, directed=True, weighted=False,
                              min_weight=0, max_weight=20):
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


def dijkstra_analysis(graph):
    execution_times = []

    for size in graph_sizes:
        graph = generate_random_graph(size, 0.12)
        execution_time = dijkstra_on_random_graph(graph)
        execution_times.append(execution_time)
        print(f"Graph of size {size} - Time taken: {execution_time} seconds")

def johnsons_analysis(graph):
    # Create a copy of the graph with an additional vertex connected to all other vertices
    extended_graph = graph.copy()
    new_vertex = max(graph.nodes) + 1
    extended_graph.add_node(new_vertex)
    for vertex in graph.nodes:
        extended_graph.add_edge(new_vertex, vertex, weight=0)

    # Run Bellman-Ford algorithm to find the shortest paths from the new vertex to all other vertices
    bellman_ford_result = nx.bellman_ford_path_length(extended_graph, new_vertex, weight='weight')

    # Update edge weights to remove negative weights
    for u, v, weight in graph.edges(data='weight', default=1):
        graph[u][v]['weight'] = weight + bellman_ford_result[u] - bellman_ford_result[v]

    # Run Dijkstra's algorithm for each vertex
    total_path_length = 0
    for start_vertex in graph.nodes:
        lengths = nx.single_source_dijkstra_path_length(graph, start_vertex, weight='weight')
        total_path_length += sum(lengths.values())

    # Calculate the average path length
    average_path_length = total_path_length / (len(graph.nodes) * (len(graph.nodes) - 1))

    return average_path_length

if __name__ == "__main__":
    graph_sizes = [10, 20, 30, 40, 50]  # You can adjust the sizes as needed
    results = []

    for size in graph_sizes:
        graph = generate_random_graph(size, 0.2, directed=True, weighted=True, min_weight=-10, max_weight=20)
        average_path_length = johnsons_analysis(graph)
        results.append(average_path_length)

    # Plotting the histogram
    plt.hist(results, bins=10, alpha=0.75, edgecolor='black')
    plt.title('Johnson\'s Algorithm Analysis')
    plt.xlabel('Average Path Length')
    plt.ylabel('Frequency')
    plt.show()

# Import necessary libraries and functions
import csv
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from disjoint_set_forest import make_set, find_set, union
import matplotlib.pyplot as plt
import numpy as np
from johnson import johnson


# Function to read data from a CSV file
def my_data(filename):
    my_list = []
    with open(filename) as dataset:
        dataset_reader = csv.reader(dataset, delimiter=",")
        for row in dataset_reader:
            my_list.append(row)
        return my_list


# Load data from the CSV file
data_list = my_data("London Underground data.csv")

# Initialize variables
ID_counter1 = 0
vertices = {}
edges = []

# Process data to create vertices and edges
for row in data_list:
    line, start_stations, end_stations, duration = row[:4]
    if start_stations not in vertices:
        vertices[start_stations] = ID_counter1
        ID_counter1 += 1

# Create edges
for row in data_list:
    line, start_stations, end_stations, duration = row[:4]
    if end_stations:
        start_stations_id = vertices[start_stations]
        end_stations_id = vertices[end_stations]
        edges.append((start_stations, end_stations, int(duration)))

# Convert the vertices dict to a list
vertices_list = list(vertices.items())

# Initialize the graph
graph = AdjacencyListGraph(len(vertices), False, True)
for edge in edges:
    start_station_id = vertices[edge[0]]
    end_station_id = vertices[edge[1]]
    duration = edge[2]

    # Check if the edge already exists before inserting
    if not graph.has_edge(start_station_id, end_station_id):
        graph.insert_edge(start_station_id, end_station_id, duration)

    # Since this is an undirected graph, insert the reverse edge as well
    if not graph.has_edge(end_station_id, start_station_id):
        graph.insert_edge(end_station_id, start_station_id, duration)


# Function to initialize Kruskal's algorithm for finding MST
def kruskal_for_closure(G):
    if G.is_directed():
        raise RuntimeError("Graph should be undirected.")

    card_V = G.get_card_V()
    # Keep an array of handles to disjoint-set objects.
    forest = [make_set(v) for v in range(card_V)]

    # Make an array of weighted edges and sort it by weight.
    edges = [(u, edge.get_v(), edge.get_weight())
             for u in range(card_V) for edge in G.get_adj_list(u) if u < edge.get_v()]

    # Initialize retained edges
    retained_edges = []

    # Examine each edge.
    for edge in edges:
        u = forest[edge[0]]
        v = forest[edge[1]]
        # If the endpoints are not in the same tree, connect the trees.
        if find_set(u) != find_set(v):
            retained_edges.append((edge[0], edge[1]))  # Record retained edge
            union(u, v)

    return retained_edges


# Function to determine closure feasibility and list affected routes
def determine_closure_feasibility(graph, vertices_list):
    # Use the kruskal function from mst.py to find the MST
    mst = kruskal(graph)
    # Retrieve the retained edges from the MST
    retained_edges = []
    for u in range(mst.get_card_V()):
        for edge in mst.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                retained_edges.append((u, v))
    # Check if closure is feasible by ensuring retained edges exist in the original graph
    feasible = all(
        graph.has_edge(u, v) or graph.has_edge(v, u) for u, v in retained_edges
    )
    # Check if closure is feasible
    if feasible:
        print("Closure can be executed.")
        print("Affected routes:")
        # Print affected routes using station names
        for u, v in retained_edges:
            station_u = vertices_list[u][0]  # Get station name for ID u
            station_v = vertices_list[v][0]  # Get station name for ID v
            print(f"{station_u} -- {station_v}")
    else:
        print("Closure is infeasible. Reason: Some station pairs become unreachable.")
        # Initialize a set to store the names of unreachable stations
        unreachable_stations = set()
        # Iterate through the list of vertices to check reachability
        for station_name, station_id in vertices_list:
            # Check if the station is reachable by any retained edge
            reachable = any(
                graph.has_edge(station_id, v) or graph.has_edge(v, station_id)
                for u, v in retained_edges
            )
            # If the station is not reachable, add it to the set of unreachable stations
            if not reachable:
                unreachable_stations.add(station_name)

        # Print the list of unreachable stations
        print("Unreachable stations:", ', '.join(unreachable_stations))


# Call the function to determine closure feasibility and list affected routes
determine_closure_feasibility(graph, vertices_list)
# Creating the Histogram

# Perform closure (assuming you have a function to perform closure)
# ...
johnson_d = johnson(graph)
# Johnson's algorithm after closure
johnson_d_post_closure = johnson(graph)

# Initialize arrays for pre-closure and post-closure data
num_stops_pre_closure = []
num_stops_post_closure = []
durations_post_closure = []

# Iterate over all station pairs
for i in range(len(vertices)):
    for j in range(len(vertices)):
        # Exclude the diagonal (station to itself)
        if i != j and not np.isinf(johnson_d[i][j]) and not np.isinf(johnson_d_post_closure[i][j]):
            num_stops_pre_closure.append(int(johnson_d[i][j]))
            num_stops_post_closure.append(int(johnson_d_post_closure[i][j]))
            durations_post_closure.append(int(johnson_d_post_closure[i][j]))

# Create histograms for comparison
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(num_stops_post_closure, bins=max(num_stops_post_closure) - min(num_stops_post_closure) + 1, color='red', edgecolor='black')
plt.title('Post-Closure - Number of Stops')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(durations_post_closure, bins=max(durations_post_closure) - min(durations_post_closure) + 1, color='green', edgecolor='black')
plt.title('Post-Closure - Journey Durations')
plt.xlabel('Journey Duration (minutes)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
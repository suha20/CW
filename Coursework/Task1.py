import csv
import time
import numpy as np
from johnson import johnson
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
import matplotlib.pyplot as plt


def my_data(filename):

    my_list = [] #initialising a list to contain the rows in the dataset

    with open(filename) as dataset:
        dataset_reader = csv.reader(dataset, delimiter=",")
        for row in dataset_reader:
            my_list.append(row)
        return my_list

data_list = my_data("London Underground data.csv")



ID_counter1 = 0
vertices = {}  # initializing dictionary of vertices
edges = []

#vertices
for row in data_list:
    line, start_stations, end_stations, duration = row[:4]

    if start_stations not in vertices:
        vertices[start_stations] = ID_counter1 #setting the value of keys(stations) as the ID numbers
        ID_counter1 += 1



#edges
for row in data_list:
    line, start_stations, end_stations, duration = row[:4]
    if end_stations:
        start_stations_id = vertices[start_stations] #assigning the dict values to the keys to the variable here
        end_stations_id = vertices[end_stations]

        #adding the edge to the list
        edges.append((start_stations, end_stations, int(duration)))






#initializing the graph

graph1 = AdjacencyListGraph(len(vertices), False, True)


for edge in edges:
    start_station_id = vertices[edge[0]]
    end_station_id = vertices[edge[1]]
    duration = edge[2]

    # Check if the edge already exists before inserting
    if not graph1.has_edge(start_station_id, end_station_id):
        graph1.insert_edge(start_station_id, end_station_id, duration)

    # Since this is an undirected graph, insert the reverse edge as well
    if not graph1.has_edge(end_station_id, start_station_id):
        graph1.insert_edge(end_station_id, start_station_id, duration)






# Funtion to initialize dijsktra algorithm

def dijkstra1 (graph1, start_station, target_station):

    valid_stations = all(station in vertices for station in [start_station, target_station])

    if valid_stations:

        start_station_index = vertices[start_station]
        target_station_index = vertices[target_station]

        d, pi = dijkstra(graph1, start_station_index)
        if pi[target_station_index] is not None:
            path = []
            current_node = target_station_index
            while current_node is not None:
                path.insert(0,list(vertices.keys())[current_node]) #if the path doesnt recognise int, put the keys here
                current_node = pi[current_node]

            print(f"Shortest path from '{start_station}' to '{target_station}': {'->'.join(path)}")
            print(f"Total duration: {d[target_station_index]} minutes")
        else :

            print("No path found")


    else:
        print("invalid station name")




start_station = input("Enter your station")
target_station = input("Enter your destination")
start_time = time.time()
dijkstra1(graph1, start_station, target_station)
end_time = time.time()
elapsed_time = end_time - start_time

# Printing the time taken in seconds.
print(f"Time taken: {elapsed_time} seconds")




## Creating the Histogram

num_vertices = len(vertices)
adjacency_matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]  # Initialize the adjacency matrix
# This line calculates the number of nodes in the graph by finding the length of the adjacency matrix.
n = len(adjacency_matrix)

# #Johnson's algorithm is applied to the graph (graph1) to compute the shortest paths between all pairs of nodes.
# The result is stored in the variable johnson_d.
johnson_d = johnson(graph1)

#The result from Johnson's algorithm is converted into a NumPy array named time_differences.
time_differences = np.array(johnson_d)

# 2D Array of time differences flattened to 1D
time_differences_flat = time_differences.flatten()

# Infinity values are removed from the flattened array
time_differences_flat = time_differences_flat[~np.isinf(time_differences_flat)]



# Histogram is created using Matplotlib, with the time differences as the data.
# It is divided into 150 bins, colored blue with black edges.
plt.hist(time_differences_flat, bins=150, color='blue', edgecolor='black')
# Adding the title and labels
plt.title('Histogram of Time Differences between Station Pairs')
#labels x-axis of histogram
plt.xlabel('Time Difference (minutes)')
#label for y axis
plt.ylabel('Frequency')
# Displays final plotted histogram
plt.show()
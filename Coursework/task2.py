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
vertices = {}
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

            print(f"Number of Stations from '{start_station}' to '{target_station}': {len(path[1:])} stations including the destination station")  # the last numerical parameter makes it print the count of stations in between
        else:
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

# Johnson's algorithm
johnson_d = johnson(graph1)

# Initialising an array to store the number of stops for each station pair
num_stops = []

# Iterating over all the station pairs
for i in range(len(vertices)):
    for j in range(len(vertices)):
        # Excluding the diagonal (station to itself)
        if i != j and not np.isinf(johnson_d[i][j]):
            num_stops.append(int(johnson_d[i][j]))

# Creating the histogram
plt.hist(num_stops, bins=max(num_stops) - min(num_stops) + 1, color='green', edgecolor='black')
# Bin count changed according to number of stops

# Adding the title and labels
plt.title('Histogram of Number of Stops between Station Pairs')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')

# Displays the final plotted histogram
plt.show()



